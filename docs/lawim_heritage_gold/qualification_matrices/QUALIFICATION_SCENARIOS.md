# QUALIFICATION SCENARIOS — LAWIM Heritage Gold

**Document ID:** LAWIM-GOLD-QM-SCENARIOS-V1
**Status:** CANONICAL — 100+ validated qualification scenarios for all request families
**Date:** 2026-07-15
**Total Scenarios:** 100+

---

## Table of Contents

1. [Residential — Studio (Scenarios 1-5)](#scenarios-1-5-residential--studio)
2. [Residential — Chambre (Scenarios 6-10)](#scenarios-6-10-residential--chambre)
3. [Residential — Appartement (Scenarios 11-20)](#scenarios-11-20-residential--appartement)
4. [Residential — Villa/Maison (Scenarios 21-28)](#scenarios-21-28-residential--villamaison)
5. [Land — Terrain titré (Scenarios 29-34)](#scenarios-29-34-land--terrain-titre)
6. [Land — Terrain non titré (Scenarios 35-38)](#scenarios-35-38-land--terrain-non-titre)
7. [Land — Other (Scenarios 39-44)](#scenarios-39-44-land--other)
8. [Commercial (Scenarios 45-52)](#scenarios-45-52-commercial)
9. [Financing (Scenarios 53-58)](#scenarios-53-58-financing)
10. [Professional (Scenarios 59-66)](#scenarios-59-66-professional)
11. [Services (Scenarios 67-74)](#scenarios-67-74-services)
12. [Listing — Mise en location (Scenarios 75-80)](#scenarios-75-80-listing--mise-en-location)
13. [Listing — Mise en vente (Scenarios 81-86)](#scenarios-81-86-listing--mise-en-vente)
14. [Special cases (Scenarios 87-100)](#scenarios-87-100-special-cases)

---

## Scenarios 1-5: Residential — Studio

## SCENARIO-001: Studio à louer Yaoundé budget 150k

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: studio
- **transaction_type**: RENT
- **requester_profile**: tenant

### initial_message
"Bonjour, je cherche un studio à Yaoundé pas trop cher, max 150 000 FCFA par mois."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: studio
- FLD-CITY: Yaoundé
- FLD-BUDGET_MAX: 150000
- FLD-BUDGET_TYPE: MONTHLY_RENT

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-DISPONIBILITE — Date d'entrée non précisée
3. FLD-MEUBLE — Non précisé si meublé ou non
4. FLD-CUISINE — Type de cuisine non spécifié

### next_question
"Bonjour ! Un studio à Yaoundé pour 150 000 FCFA, très bien. Dans quel quartier de Yaoundé cherchez-vous ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer intention et type de bien
- Demander le quartier
- Préparer l'initialisation du moteur de matching

### forbidden_actions
- Lancer la recherche sans quartier
- Demander les coordonnées personnelles
- Demander des détails excessifs sur les équipements

### matching_criteria
- FLD-CITY: hard_constraint + weight 30
- FLD-BUDGET_MAX: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 20

---

## SCENARIO-002: Studio à Douala budget 100k

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: studio
- **transaction_type**: RENT
- **requester_profile**: étudiant

### initial_message
"S'il vous plaît je cherche un studio à Douala, mon budget c'est 100 000 maximum."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: studio
- FLD-CITY: Douala
- FLD-BUDGET_MAX: 100000
- FLD-BUDGET_TYPE: MONTHLY_RENT

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-DISPONIBILITE — Disponibilité non précisée
3. FLD-MEUBLE — Non précisé
4. FLD-CUISINE — Non spécifié

### next_question
"D'accord, un studio à Douala avec un budget de 100 000 FCFA. Vous avez une préférence pour un quartier en particulier ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer ville et budget
- Demander le quartier
- Vérifier si le budget est réalisable pour un studio à Douala

### forbidden_actions
- Lancer la recherche sans quartier
- Proposer des biens hors budget

### matching_criteria
- FLD-CITY: hard_constraint + weight 30
- FLD-BUDGET_MAX: hard_constraint + weight 30
- FLD-PROPERTY_TYPE: hard_constraint + weight 20

---

## SCENARIO-003: Studio meublé à louer

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: studio_meuble
- **transaction_type**: RENT
- **requester_profile**: jeune professionnel

### initial_message
"Hello, I'm looking for a furnished studio in Douala, Bonapriso area. Budget around 200k."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: studio_meuble
- FLD-CITY: Douala
- FLD-NEIGHBORHOOD: Bonapriso
- FLD-BUDGET_MAX: 200000
- FLD-BUDGET_TYPE: MONTHLY_RENT

### missing_fields (ordered by priority)
1. FLD-DISPONIBILITE — Date d'entrée souhaitée
2. FLD-CUISINE — Type de cuisine non précisé
3. FLD-DOUCHES — Préférence douche interne/externe

### next_question
"Perfect! A furnished studio in Bonapriso, Douala for 200k. When would you like to move in?"

### readiness_level
MINIMUM_SEARCH_READY

### allowed_actions
- Lancer la recherche immédiate
- Présenter les résultats
- Proposer des critères de raffinement

### forbidden_actions
- Continuer à poser des questions avant la recherche
- Demander les coordonnées avant les résultats

### matching_criteria
- FLD-CITY: hard_constraint + weight 30
- FLD-NEIGHBORHOOD: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-PROPERTY_TYPE: hard_constraint + weight 15

---

## SCENARIO-004: Studio à Bafoussam

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: studio
- **transaction_type**: RENT
- **requester_profile**: fonctionnaire muté

### initial_message
"Je suis muté à Bafoussam, je cherche un studio pas cher pour commencer."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: studio
- FLD-CITY: Bafoussam

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-NEIGHBORHOOD — Quartier non précisé
3. FLD-DISPONIBILITE — Disponibilité non précisée
4. FLD-MEUBLE — Non précisé

### next_question
"Bienvenue à Bafoussam ! Je peux vous aider à trouver un studio. Quel est votre budget maximum par mois ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Confirmer la ville
- Demander le budget
- Proposer une aide à la recherche

### forbidden_actions
- Lancer la recherche sans budget
- Demander des documents personnels

### matching_criteria
- FLD-CITY: hard_constraint + weight 35
- FLD-PROPERTY_TYPE: hard_constraint + weight 25

---

## SCENARIO-005: Studio avec douche externe

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: studio
- **transaction_type**: RENT
- **requester_profile**: travailleur

### initial_message
"Je cherche un studio à Yaoundé avec douche externe, pas cher, maximum 80 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: studio
- FLD-CITY: Yaoundé
- FLD-BUDGET_MAX: 80000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-DOUCHES: EXTERNE

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-DISPONIBILITE — Date d'entrée
3. FLD-CUISINE — Type de cuisine

### next_question
"Un studio à Yaoundé avec douche externe pour 80 000 FCFA. Dans quel quartier cherchez-vous ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer ville, budget, type de douche
- Demander le quartier
- Vérifier disponibilités

### forbidden_actions
- Proposer des studios avec douche interne seulement
- Ignorer la préférence douche externe

### matching_criteria
- FLD-CITY: hard_constraint + weight 30
- FLD-BUDGET_MAX: hard_constraint + weight 25
- FLD-DOUCHES: hard_constraint + weight 20

---

## Scenarios 6-10: Residential — Chambre

## SCENARIO-006: Chambre simple à Yaoundé

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: chambre_simple
- **transaction_type**: RENT
- **requester_profile**: étudiant

### initial_message
"Je cherche une chambre simple à Yaoundé près de l'université."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: chambre_simple
- FLD-CITY: Yaoundé

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier approximatif (près université)
2. FLD-BUDGET_MAX — Budget non mentionné
3. FLD-DISPONIBILITE — Disponibilité non précisée
4. FLD-PROXIMITY_PREFERENCES — Proximité université à préciser

### next_question
"Parfait ! Une chambre simple près de l'université à Yaoundé. Quel est votre budget maximum par mois ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander le budget
- Clarifier le quartier (université de Yaoundé I ou II ?)
- Demander la date d'entrée

### forbidden_actions
- Lancer la recherche sans budget
- Proposer des chambres hors zone universitaire

### matching_criteria
- FLD-CITY: hard_constraint + weight 30
- FLD-PROPERTY_TYPE: hard_constraint + weight 25

---

## SCENARIO-007: Chambre moderne avec douche interne

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: chambre_moderne
- **transaction_type**: RENT
- **requester_profile**: jeune travailleur

### initial_message
"Bonsoir, je recherche une chambre moderne avec douche interne à Douala, pas plus de 120 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: chambre_moderne
- FLD-CITY: Douala
- FLD-BUDGET_MAX: 120000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-DOUCHES: INTERNE

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-DISPONIBILITE — Disponibilité non précisée
3. FLD-MEUBLE — Non précisé si meublée ou non

### next_question
"Bonsoir ! Une chambre moderne avec douche interne à Douala pour 120 000 FCFA. Dans quel quartier souhaitez-vous être ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer intention et budget
- Demander le quartier
- Préciser le type de douche

### forbidden_actions
- Proposer des chambres sans douche interne
- Demander des informations personnelles

### matching_criteria
- FLD-CITY: hard_constraint + weight 30
- FLD-BUDGET_MAX: hard_constraint + weight 25
- FLD-DOUCHES: hard_constraint + weight 20

---

## SCENARIO-008: Chambre budget très limité

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: chambre_simple
- **transaction_type**: RENT
- **requester_profile**: étudiant boursier

### initial_message
"Je suis étudiant, je cherche une chambre pas chère à Yaoundé, max 25 000 par mois."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: chambre_simple
- FLD-CITY: Yaoundé
- FLD-BUDGET_MAX: 25000
- FLD-BUDGET_TYPE: MONTHLY_RENT

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-DISPONIBILITE — Disponibilité
3. FLD-PROXIMITY_PREFERENCES — Proximité université ou transports

### next_question
"D'accord, une chambre simple à Yaoundé pour 25 000 FCFA. C'est un budget serré. Puis-je savoir dans quel quartier ou secteur vous cherchez ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer intention
- Avertir que le budget est limité pour ce type
- Proposer des alternatives (cité universitaire)
- Demander le quartier

### forbidden_actions
- Proposer des chambres au-dessus du budget
- Ignorer la contrainte budgétaire

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 35

---

## SCENARIO-009: Chambre cité universitaire

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: cite_universitaire
- **transaction_type**: RENT
- **requester_profile**: étudiant

### initial_message
"Salut, je cherche une chambre en cité universitaire à Douala pour la rentrée."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: cite_universitaire
- FLD-CITY: Douala

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-NEIGHBORHOOD — Secteur ou université précise
3. FLD-DISPONIBILITE — Date de rentrée à préciser
4. FLD-DUREE — Durée du séjour

### next_question
"Salut ! Une chambre en cité universitaire à Douala. C'est pour quelle université précisément et quel est votre budget ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Clarifier l'université
- Demander le budget
- Demander la date d'entrée

### forbidden_actions
- Lancer la recherche sans budget
- Proposer des logements hors campus

### matching_criteria
- FLD-CITY: hard_constraint + weight 30
- FLD-PROPERTY_TYPE: hard_constraint + weight 30

---

## SCENARIO-010: Chambre avec accès cuisine

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: chambre_moderne
- **transaction_type**: RENT
- **requester_profile**: ouvrier

### initial_message
"Je cherche une chambre où je peux cuisiner, avec cuisine partagée ou kitchenette, à Douala, max 70 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: chambre_moderne
- FLD-CITY: Douala
- FLD-BUDGET_MAX: 70000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-CUISINE: PARTAGEE_OU_KITCHENETTE

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-DOUCHES — Type de douche non précisé
3. FLD-DISPONIBILITE — Disponibilité

### next_question
"Je comprends, une chambre avec accès cuisine à Douala pour 70 000 FCFA. Vous avez un quartier préféré ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer le besoin cuisine
- Demander le quartier
- Vérifier le type de douche

### forbidden_actions
- Proposer des chambres sans accès cuisine
- Ignorer la préférence cuisine

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 25
- FLD-CUISINE: hard_constraint + weight 20

---

## Scenarios 11-20: Residential — Appartement

## SCENARIO-011: Appartement 2 chambres Douala

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: appartement_non_meuble
- **transaction_type**: RENT
- **requester_profile**: famille

### initial_message
"Bonjour, nous sommes une famille de 4 personnes, nous cherchons un appartement 2 chambres à Douala, quartier Bonamoussadi."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: appartement_non_meuble
- FLD-CITY: Douala
- FLD-NEIGHBORHOOD: Bonamoussadi
- FLD-CHAMBRES: 2
- FLD-OCCUPANTS: 4

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-DISPONIBILITE — Date d'entrée
3. FLD-SALONS — Nombre de salons
4. FLD-DOUCHES — Nombre de douches

### next_question
"Bonjour ! Un appartement 2 chambres à Bonamoussadi pour une famille de 4 personnes. Quel est votre budget maximum par mois ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander le budget
- Confirmer quartier et nombre de chambres
- Proposer des options adaptées

### forbidden_actions
- Lancer la recherche sans budget
- Ignorer le nombre d'occupants

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-NEIGHBORHOOD: hard_constraint + weight 20
- FLD-CHAMBRES: hard_constraint + weight 20

---

## SCENARIO-012: Appartement meublé Yaoundé

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: appartement_meuble
- **transaction_type**: RENT
- **requester_profile**: expatrié

### initial_message
"I'm looking for a furnished 1-bedroom apartment in Yaoundé, Bastos area. Budget up to 500k."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: appartement_meuble
- FLD-CITY: Yaoundé
- FLD-NEIGHBORHOOD: Bastos
- FLD-BUDGET_MAX: 500000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-CHAMBRES: 1

### missing_fields (ordered by priority)
1. FLD-DISPONIBILITE — Move-in date
2. FLD-SALONS — Living room preference
3. FLD-DOUCHES — Bathroom preference

### next_question
"Great! A furnished 1-bedroom in Bastos, Yaoundé for 500k. When would you like to move in?"

### readiness_level
MINIMUM_SEARCH_READY

### allowed_actions
- Launch search immediately
- Present results
- Ask for refinement criteria

### forbidden_actions
- Continue asking questions before search
- Ask for contact details before results

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-NEIGHBORHOOD: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-PROPERTY_TYPE: hard_constraint + weight 15

---

## SCENARIO-013: Appartement 3 chambres avec salon

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: appartement_non_meuble
- **transaction_type**: RENT
- **requester_profile**: famille nombreuse

### initial_message
"Bonjour, je cherche un appartement 3 chambres avec grand salon à Douala, pas plus de 250 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: appartement_non_meuble
- FLD-CITY: Douala
- FLD-BUDGET_MAX: 250000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-CHAMBRES: 3
- FLD-SALONS: 1

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-DISPONIBILITE — Disponibilité
3. FLD-DOUCHES — Nombre de douches

### next_question
"Bonjour ! Un 3 chambres avec salon à Douala pour 250 000 FCFA. Dans quel quartier cherchez-vous ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer nombre de pièces et budget
- Demander le quartier
- Préparer la recherche

### forbidden_actions
- Proposer des appartements sans salon
- Ignorer le nombre de chambres

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-CHAMBRES: hard_constraint + weight 20
- FLD-SALONS: hard_constraint + weight 15

---

## SCENARIO-014: Appartement avec parking et ascenseur

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: appartement_meuble
- **transaction_type**: RENT
- **requester_profile**: cadre supérieur

### initial_message
"Je recherche un appartement 2 chambres avec parking et ascenseur à Douala, quartier Akwa, budget 400 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: appartement_meuble
- FLD-CITY: Douala
- FLD-NEIGHBORHOOD: Akwa
- FLD-BUDGET_MAX: 400000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-CHAMBRES: 2
- FLD-PARKING: OUI
- FLD-ASCENSEUR: OUI

### missing_fields (ordered by priority)
1. FLD-DISPONIBILITE — Disponibilité
2. FLD-ETAGE — Étage souhaité
3. FLD-SECURITE — Sécurité de l'immeuble

### next_question
"Parfait ! Un 2 chambres avec parking et ascenseur à Akwa pour 400 000 FCFA. Quand souhaitez-vous emménager ?"

### readiness_level
MINIMUM_SEARCH_READY

### allowed_actions
- Lancer la recherche immédiatement
- Filtrer les biens avec parking et ascenseur
- Présenter les résultats

### forbidden_actions
- Demander des informations personnelles avant les résultats
- Proposer des biens sans parking ou ascenseur

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-NEIGHBORHOOD: hard_constraint + weight 20
- FLD-BUDGET_MAX: hard_constraint + weight 15
- FLD-PARKING: hard_constraint + weight 15
- FLD-ASCENSEUR: hard_constraint + weight 10

---

## SCENARIO-015: Appartement de luxe budget élevé

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: appartement_meuble
- **transaction_type**: RENT
- **requester_profile**: expatrié/diaspora

### initial_message
"Je cherche un appartement de luxe meublé à Yaoundé, minimum 3 chambres, avec climatisation, groupe électrogène et vue. Budget 1 500 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: appartement_meuble
- FLD-CITY: Yaoundé
- FLD-BUDGET_MAX: 1500000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-CHAMBRES: 3
- FLD-CLIMATISATION: OUI
- FLD-GROUPE_ELECTROGENE: OUI

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-DISPONIBILITE — Disponibilité
3. FLD-SECURITE — Sécurité
4. FLD-PISCINE — Piscine souhaitée ?

### next_question
"Très bien ! Un appartement de luxe 3 chambres meublé à Yaoundé pour 1 500 000 FCFA. Dans quel quartier souhaitez-vous être ? Bastos, Mvog-Mbi ou un autre ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer le budget élevé
- Demander le quartier
- Lister les équipements de luxe disponibles

### forbidden_actions
- Proposer des biens standards ou bas de gamme
- Demander des documents sans présenter de biens

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-BUDGET_MAX: hard_constraint + weight 25
- FLD-CHAMBRES: hard_constraint + weight 15
- FLD-CLIMATISATION: soft_constraint + weight 10

---

## SCENARIO-016: Appartement courte durée

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: appartement_courte_duree
- **transaction_type**: RENT
- **requester_profile**: voyageur d'affaires

### initial_message
"Bonjour, je cherche un appartement meublé à Douala pour 2 semaines, début août."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: appartement_courte_duree
- FLD-CITY: Douala
- FLD-DISPONIBILITE: début août
- FLD-DUREE: 2 semaines
- FLD-MEUBLE: OUI

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-NEIGHBORHOOD — Quartier non mentionné
3. FLD-NOMBRE_VOYAGEURS — Nombre de personnes

### next_question
"Bonjour ! Un appartement meublé à Douala pour 2 semaines début août. Quel est votre budget par nuit ou pour le séjour ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Confirmer la courte durée
- Demander le budget
- Préciser le quartier

### forbidden_actions
- Proposer des baux longue durée
- Demander des garanties locatives classiques

### matching_criteria
- FLD-CITY: hard_constraint + weight 30
- FLD-PROPERTY_TYPE: hard_constraint + weight 25
- FLD-DUREE: hard_constraint + weight 15

---

## SCENARIO-017: Appartement non meublé longue durée

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: appartement_non_meuble
- **transaction_type**: RENT
- **requester_profile**: famille

### initial_message
"Je cherche un appartement 2 chambres vide à Yaoundé, contrat longue durée, max 150 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: appartement_non_meuble
- FLD-CITY: Yaoundé
- FLD-BUDGET_MAX: 150000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-CHAMBRES: 2
- FLD-MEUBLE: NON
- FLD-DUREE: LONGUE_DUREE

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-DISPONIBILITE — Date d'entrée
3. FLD-SALONS — Salon souhaité
4. FLD-DOUCHES — Salle de bain

### next_question
"Un 2 chambres vide à Yaoundé pour 150 000 FCFA en longue durée. Dans quel quartier préférez-vous ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer les besoins
- Demander le quartier
- Préparer la recherche

### forbidden_actions
- Proposer des meublés sans demander
- Ignorer la préférence longue durée

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-CHAMBRES: hard_constraint + weight 20

---

## SCENARIO-018: Colocation appartement

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: colocation
- **transaction_type**: RENT
- **requester_profile**: étudiant

### initial_message
"Je cherche une colocation à Douala, max 80 000 par mois, près de l'Université de Douala."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: colocation
- FLD-CITY: Douala
- FLD-BUDGET_MAX: 80000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-PROXIMITY_PREFERENCES: Université de Douala

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier précis près de l'université
2. FLD-DISPONIBILITE — Disponibilité
3. FLD-GENRE_COLOCATION — Mixte, hommes, femmes ?
4. FLD-NOMBRE_COLOCATAIRES — Nombre de colocataires souhaité

### next_question
"Une colocation près de l'Université de Douala pour 80 000 FCFA. Vous préférez une colocation mixte, hommes ou femmes ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander le quartier précis
- Préciser le type de colocation
- Vérifier le budget

### forbidden_actions
- Proposer des appartements privés (non colocation)
- Ignorer les préférences de colocation

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-PROPERTY_TYPE: hard_constraint + weight 25

---

## SCENARIO-019: Appartement 1 chambre meublé vue mer

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: appartement_meuble
- **transaction_type**: RENT
- **requester_profile**: professionnel

### initial_message
"Je veux un appartement 1 chambre meublé avec vue sur mer à Douala, je peux mettre jusqu'à 600 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: appartement_meuble
- FLD-CITY: Douala
- FLD-BUDGET_MAX: 600000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-CHAMBRES: 1
- FLD-VUE: MER

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier (Bonanjo, Bonapriso ?)
2. FLD-DISPONIBILITE — Disponibilité
3. FLD-ETAGE — Étage (vue mer nécessite étage élevé)

### next_question
"Un 1 chambre meublé avec vue sur mer à Douala pour 600 000 FCFA. Dans quel quartier ? Bonanjo ou Bonapriso par exemple ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer la vue mer
- Demander le quartier
- Vérifier la faisabilité

### forbidden_actions
- Proposer des appartements sans vue mer
- Ignorer la préférence de vue

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-CHAMBRES: hard_constraint + weight 15
- FLD-VUE: hard_constraint + weight 15

---

## SCENARIO-020: Appartement avec jardin

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: appartement_non_meuble
- **transaction_type**: RENT
- **requester_profile**: famille avec enfants

### initial_message
"Bonjour, je cherche un appartement 3 chambres avec un petit jardin pour les enfants à Yaoundé, 200 000 max."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: appartement_non_meuble
- FLD-CITY: Yaoundé
- FLD-BUDGET_MAX: 200000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-CHAMBRES: 3
- FLD-JARDIN: OUI

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-DISPONIBILITE — Disponibilité
3. FLD-SECURITE — Sécurité pour enfants
4. FLD-SALONS — Salon familial

### next_question
"Bonjour ! Un 3 chambres avec jardin à Yaoundé pour 200 000 FCFA. Dans quel quartier cherchez-vous ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander le quartier
- Noter le besoin de jardin
- Préparer recherche adaptée

### forbidden_actions
- Proposer des appartements sans extérieur
- Ignorer le besoin pour enfants

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-CHAMBRES: hard_constraint + weight 20
- FLD-JARDIN: hard_constraint + weight 15

---

## Scenarios 21-28: Residential — Villa/Maison

## SCENARIO-021: Villa 4 chambres Yaoundé

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: villa
- **transaction_type**: RENT
- **requester_profile**: famille aisée

### initial_message
"Je cherche une villa 4 chambres à Yaoundé, quartier Mvog-Mbi, budget 500 000 à 700 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: villa
- FLD-CITY: Yaoundé
- FLD-NEIGHBORHOOD: Mvog-Mbi
- FLD-BUDGET_MAX: 700000
- FLD-BUDGET_MIN: 500000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-CHAMBRES: 4

### missing_fields (ordered by priority)
1. FLD-DISPONIBILITE — Disponibilité
2. FLD-SALONS — Nombre de salons
3. FLD-DOUCHES — Nombre de douches
4. FLD-PARKING — Parking souhaité ?
5. FLD-CUISINE — Type de cuisine

### next_question
"Une villa 4 chambres à Mvog-Mbi, Yaoundé, entre 500 000 et 700 000 FCFA. Quand souhaitez-vous emménager ?"

### readiness_level
MINIMUM_SEARCH_READY

### allowed_actions
- Lancer la recherche immédiatement
- Filtrer les villas 4 chambres à Mvog-Mbi
- Présenter les résultats

### forbidden_actions
- Continuer à poser des questions avant la recherche
- Demander les coordonnées

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-NEIGHBORHOOD: hard_constraint + weight 20
- FLD-BUDGET_MAX: hard_constraint + weight 15
- FLD-CHAMBRES: hard_constraint + weight 20

---

## SCENARIO-022: Villa basse avec cour et parking

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: villa_basse
- **transaction_type**: RENT
- **requester_profile**: famille

### initial_message
"Bonjour, je cherche une villa basse avec une grande cour et parking à Douala, max 350 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: villa_basse
- FLD-CITY: Douala
- FLD-BUDGET_MAX: 350000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-PARKING: OUI
- FLD-COUR: OUI

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-CHAMBRES — Nombre de chambres non précisé
3. FLD-DISPONIBILITE — Disponibilité
4. FLD-SALONS — Salon souhaité

### next_question
"Une villa basse avec cour et parking à Douala pour 350 000 FCFA. Dans quel quartier et combien de chambres souhaitez-vous ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer cour et parking
- Demander quartier et chambres
- Vérifier le budget

### forbidden_actions
- Proposer des villas sans cour ou parking
- Proposer des villas étages (pas basses)

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-PROPERTY_TYPE: hard_constraint + weight 20

---

## SCENARIO-023: Maison individuelle avec jardin

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: maison_individuelle
- **transaction_type**: RENT
- **requester_profile**: famille

### initial_message
"Je cherche une maison individuelle avec un jardin à Buea, calme, pas trop cher."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: maison_individuelle
- FLD-CITY: Buea
- FLD-JARDIN: OUI
- FLD-CALME: OUI

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-NEIGHBORHOOD — Quartier non mentionné
3. FLD-CHAMBRES — Nombre de chambres non précisé
4. FLD-DISPONIBILITE — Disponibilité

### next_question
"Une maison individuelle avec jardin à Buea, au calme. Quel est votre budget maximum par mois ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander le budget
- Préciser le quartier
- Demander le nombre de chambres

### forbidden_actions
- Lancer la recherche sans budget
- Proposer des propriétés sans jardin

### matching_criteria
- FLD-CITY: hard_constraint + weight 30
- FLD-PROPERTY_TYPE: hard_constraint + weight 25

---

## SCENARIO-024: Duplex à louer

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: duplex
- **transaction_type**: RENT
- **requester_profile**: cadre

### initial_message
"Salut, je cherche un duplex meublé à Douala, Bonapriso, budget 600 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: duplex
- FLD-CITY: Douala
- FLD-NEIGHBORHOOD: Bonapriso
- FLD-BUDGET_MAX: 600000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-MEUBLE: OUI

### missing_fields (ordered by priority)
1. FLD-CHAMBRES — Nombre de chambres non précisé
2. FLD-DISPONIBILITE — Disponibilité
3. FLD-PARKING — Parking souhaité ?
4. FLD-ETAGE — Quel étage ?

### next_question
"Un duplex meublé à Bonapriso pour 600 000 FCFA. Combien de chambres souhaitez-vous ?"

### readiness_level
MINIMUM_SEARCH_READY

### allowed_actions
- Lancer la recherche
- Filtrer duplex à Bonapriso
- Demander précisions sur les pièces

### forbidden_actions
- Proposer des appartements (pas duplex)
- Ignorer le caractère meublé

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-NEIGHBORHOOD: hard_constraint + weight 20
- FLD-BUDGET_MAX: hard_constraint + weight 15
- FLD-PROPERTY_TYPE: hard_constraint + weight 20

---

## SCENARIO-025: Triplex en vente

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: triplex
- **transaction_type**: BUY
- **requester_profile**: investisseur

### initial_message
"Je cherche un triplex à acheter à Yaoundé, quartier Bastos, budget 80 millions."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: triplex
- FLD-CITY: Yaoundé
- FLD-NEIGHBORHOOD: Bastos
- FLD-BUDGET_MAX: 80000000
- FLD-BUDGET_TYPE: TOTAL_PRICE

### missing_fields (ordered by priority)
1. FLD-DISPONIBILITE — Délai d'achat
2. FLD-CHAMBRES — Nombre de chambres
3. FLD-SURFACE — Surface habitable
4. FLD-FINANCING — Comptant ou crédit
5. FLD-USAGE — Résidence ou investissement

### next_question
"Un triplex à Bastos, Yaoundé pour 80 millions. C'est pour y habiter ou pour investir ?"

### readiness_level
MINIMUM_SEARCH_READY

### allowed_actions
- Lancer la recherche
- Présenter les triplex disponibles
- Discuter des options de financement

### forbidden_actions
- Proposer autres types de biens
- Négliger la question de l'usage

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-NEIGHBORHOOD: hard_constraint + weight 20
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-PROPERTY_TYPE: hard_constraint + weight 20

---

## SCENARIO-026: Villa avec piscine

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: villa
- **transaction_type**: RENT
- **requester_profile**: diaspora

### initial_message
"Hello, I'm in the diaspora and looking for a luxury villa with swimming pool in Yaoundé for when I come back. Budget around 1.2 million per month."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: villa
- FLD-CITY: Yaoundé
- FLD-BUDGET_MAX: 1200000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-PISCINE: OUI
- FLD-DIASPORA: OUI

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-CHAMBRES — Nombre de chambres
3. FLD-DISPONIBILITE — Période de retour
4. FLD-DUREE — Durée du séjour

### next_question
"Hello! A luxury villa with pool in Yaoundé for 1.2M monthly. Which neighborhood do you prefer? Bastos, Mvog-Mbi or others?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer diaspora
- Demander quartier
- Préparer options luxe

### forbidden_actions
- Proposer des villas sans piscine
- Négliger le statut diaspora (accompagnement spécifique)

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-PISCINE: hard_constraint + weight 20
- FLD-DIASPORA: ranking_preference + weight 15

---

## SCENARIO-027: Maison de ville centre-ville

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: maison_de_ville
- **transaction_type**: RENT
- **requester_profile**: commerçant

### initial_message
"Je cherche une maison de ville à Douala centre-ville, pour habiter et avoir mon bureau au rez-de-chaussée."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: maison_de_ville
- FLD-CITY: Douala
- FLD-ZONE: centre-ville
- FLD-USAGE: MIXTE (habitation + bureau)

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-NEIGHBORHOOD — Quartier précis
3. FLD-CHAMBRES — Nombre de chambres
4. FLD-DISPONIBILITE — Disponibilité
5. FLD-SURFACE_COMMERCIALE — Surface du rez-de-chaussée

### next_question
"Une maison de ville au centre-ville de Douala pour habiter et travailler. Quel est votre budget maximum par mois ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander le budget
- Préciser le quartier
- Noter l'usage mixte

### forbidden_actions
- Proposer des maisons sans espace commercial
- Négliger l'aspect professionnel

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 25
- FLD-USAGE: hard_constraint + weight 20

---

## SCENARIO-028: Villa sécurisée avec gardien

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: villa
- **transaction_type**: RENT
- **requester_profile**: diplomate

### initial_message
"I need a secure villa with 24h security and guard in Yaoundé, minimum 5 bedrooms. Budget up to 2 million."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: villa
- FLD-CITY: Yaoundé
- FLD-BUDGET_MAX: 2000000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-CHAMBRES: 5
- FLD-SECURITE: OUI
- FLD-GARDIEN: OUI

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-DISPONIBILITE — Disponibilité
3. FLD-PARKING — Parking
4. FLD-DOUCHES — Nombre de douches

### next_question
"A secure 5-bedroom villa with guard in Yaoundé for 2M. Which neighborhood do you prefer? Bastos or Mvog-Mbi are very secure areas."

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer le besoin de sécurité
- Demander le quartier
- Préparer les options haut de gamme

### forbidden_actions
- Proposer des villas sans sécurité
- Négliger le nombre de chambres

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-CHAMBRES: hard_constraint + weight 20
- FLD-SECURITE: hard_constraint + weight 20

---

## Scenarios 29-34: Land — Terrain titré

## SCENARIO-029: Terrain titré individuel Yaoundé

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_titre
- **transaction_type**: BUY
- **requester_profile**: particulier

### initial_message
"Bonjour, je cherche un terrain titré à Yaoundé, côté Mvog-Mbi ou Nkolbisson, pour construire ma maison."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_titre
- FLD-CITY: Yaoundé
- FLD-NEIGHBORHOOD: Mvog-Mbi ou Nkolbisson
- FLD-USAGE: RESIDENCE

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE — Surface recherchée
3. FLD-DISPONIBILITE — Délai d'achat
4. FLD-TITRE_FONCIER — Type de titre attendu

### next_question
"Un terrain titré à Mvog-Mbi ou Nkolbisson pour construction. Quelle surface recherchez-vous et quel est votre budget ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander surface et budget
- Vérifier le type de titre
- Préparer les options

### forbidden_actions
- Proposer des terrains non titrés
- Négliger la question du titre foncier

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 25
- FLD-NEIGHBORHOOD: hard_constraint + weight 20

---

## SCENARIO-030: Terrain titré collectif plusieurs signataires

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_titre
- **transaction_type**: BUY
- **requester_profile**: groupe d'investisseurs

### initial_message
"Nous sommes un groupe de 3 associés, nous cherchons un grand terrain titré à Douala pour construire un immeuble de rapport."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_titre
- FLD-CITY: Douala
- FLD-USAGE: INVESTISSEMENT
- FLD-NOMBRE_SIGNATAIRES: 3

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE — Surface recherchée
3. FLD-NEIGHBORHOOD — Quartier non mentionné
4. FLD-DISPONIBILITE — Délai d'achat
5. FLD-IDENTITE_SIGNATAIRES — Identité des signataires

### next_question
"Un terrain titré à Douala pour construire un immeuble de rapport pour 3 associés. Quelle surface cherchez-vous et quel est votre budget ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander surface et budget
- Noter le nombre de signataires
- Préparer les aspects légaux

### forbidden_actions
- Proposer des terrains sans titre
- Ignorer la situation de groupe

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 25
- FLD-USAGE: hard_constraint + weight 20

---

## SCENARIO-031: Terrain avec titre foncier numéro connu

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_titre
- **transaction_type**: BUY
- **requester_profile**: investisseur informé

### initial_message
"Je cherche spécifiquement un terrain qui a déjà un titre foncier, pas une simple attestation. Numéro TF obligatoire."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_titre
- FLD-TITRE_FONCIER: OUI
- FLD-NUM_TITRE_REQUIS: OUI

### missing_fields (ordered by priority)
1. FLD-CITY — Ville non mentionnée
2. FLD-BUDGET_MAX — Budget non mentionné
3. FLD-SURFACE — Surface recherchée
4. FLD-NEIGHBORHOOD — Quartier non mentionné

### next_question
"Compris, vous voulez un terrain avec titre foncier numéroté. Dans quelle ville et quel est votre budget ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander la ville
- Demander le budget
- Rassurer sur l'exigence du TF

### forbidden_actions
- Proposer des terrains sans titre foncier
- Minimiser l'importance du TF

### matching_criteria
- FLD-PROPERTY_TYPE: hard_constraint + weight 30
- FLD-TITRE_FONCIER: hard_constraint + weight 30

---

## SCENARIO-032: Terrain titré avec bornage

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_titre
- **transaction_type**: BUY
- **requester_profile**: particulier exigeant

### initial_message
"Je cherche un terrain titré déjà borné à Bafoussam, tranquille, pour construire ma villa."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_titre
- FLD-CITY: Bafoussam
- FLD-BORNAGE: OUI
- FLD-USAGE: RESIDENCE

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE — Surface recherchée
3. FLD-NEIGHBORHOOD — Quartier non mentionné
4. FLD-DISPONIBILITE — Délai d'achat

### next_question
"Un terrain titré déjà borné à Bafoussam pour construire votre villa. Quelle surface et quel budget ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander surface et budget
- Noter l'exigence de bornage
- Proposer des professionnels (géomètre)

### forbidden_actions
- Proposer des terrains non bornés
- Ignorer la demande de bornage

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 25
- FLD-BORNAGE: hard_constraint + weight 20

---

## SCENARIO-033: Terrain titré loti

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_titre
- **transaction_type**: BUY
- **requester_profile**: promoteur

### initial_message
"Je cherche un lot de terrain titré dans un lotissement à Yaoundé, 300 m² minimum."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_titre
- FLD-CITY: Yaoundé
- FLD-SURFACE_MIN: 300
- FLD-LOTI: OUI

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-NEIGHBORHOOD — Quartier ou secteur
3. FLD-DISPONIBILITE — Délai
4. FLD-VOIRIE — Voirie et réseaux

### next_question
"Un lot de terrain titré de 300 m² minimum dans un lotissement à Yaoundé. Quel budget et dans quel secteur ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander budget et secteur
- Confirmer le caractère loti
- Vérifier la disponibilité

### forbidden_actions
- Proposer des terrains non lotis
- Ignorer la surface minimum

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-SURFACE_MIN: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 20

---

## SCENARIO-034: Terrain titré pour construction résidentielle

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_titre
- **transaction_type**: BUY
- **requester_profile**: futur propriétaire

### initial_message
"Je veux acheter un terrain pour y construire ma maison. Il me faut un titre foncier propre, à Douala."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_titre
- FLD-CITY: Douala
- FLD-USAGE: RESIDENCE

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE — Surface non précisée
3. FLD-NEIGHBORHOOD — Quartier non mentionné
4. FLD-DISPONIBILITE — Délai

### next_question
"Un terrain avec titre foncier propre à Douala pour construction. Quel budget maximum et quelle surface minimum ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander budget et surface
- Rassurer sur le titre foncier
- Proposer des quartiers résidentiels

### forbidden_actions
- Proposer des terrains sans titre
- Ignorer la destination résidentielle

### matching_criteria
- FLD-CITY: hard_constraint + weight 30
- FLD-PROPERTY_TYPE: hard_constraint + weight 25
- FLD-USAGE: hard_constraint + weight 20

---

## Scenarios 35-38: Land — Terrain non titré

## SCENARIO-035: Terrain non titré avec certificat

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_non_titre
- **transaction_type**: BUY
- **requester_profile**: particulier budget limité

### initial_message
"Bonjour, je cherche un terrain pas cher à Yaoundé, avec certificat de propriété au moins, pas besoin de titre foncier."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_non_titre
- FLD-CITY: Yaoundé
- FLD-DOCUMENT: CERTIFICAT_PROPRIETE

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE — Surface non précisée
3. FLD-NEIGHBORHOOD — Quartier non mentionné
4. FLD-DISPONIBILITE — Délai

### next_question
"Un terrain avec certificat de propriété à Yaoundé. Quel budget maximum et quelle surface ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander budget et surface
- Clarifier le type de document
- Proposer des options adaptées

### forbidden_actions
- Proposer des terrains sans aucun document
- Négliger l'importance des documents

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 25
- FLD-DOCUMENT: hard_constraint + weight 20

---

## SCENARIO-036: Terrain non titré sans document

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_non_titre
- **transaction_type**: BUY
- **requester_profile**: acheteur pressé

### initial_message
"Je cherche un terrain à Douala pas cher, même sans papier, je régulariserai après."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_non_titre
- FLD-CITY: Douala
- FLD-DOCUMENT: AUCUN

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE — Surface non précisée
3. FLD-NEIGHBORHOOD — Quartier non mentionné
4. FLD-DISPONIBILITE — Délai

### next_question
"Je comprends, un terrain à Douala. Avant de chercher, sachez que LAWIM vous recommande d'avoir au moins un certificat de propriété pour sécuriser votre achat. Quel budget maximum ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Conseiller sur les risques
- Demander budget et surface
- Proposer des options avec document si possible

### forbidden_actions
- Encourager l'achat sans document
- Proposer des terrains litigieux

### matching_criteria
- FLD-CITY: hard_constraint + weight 30
- FLD-PROPERTY_TYPE: hard_constraint + weight 25

---

## SCENARIO-037: Terrain non loti axe rural

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_non_titre
- **transaction_type**: BUY
- **requester_profile**: agriculteur

### initial_message
"Bonjour, je cherche un terrain pas cher en zone rurale près de Mbalmayo pour l'agriculture."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_non_titre
- FLD-CITY: Mbalmayo
- FLD-USAGE: AGRICOLE
- FLD-ZONE: RURALE

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE — Surface non précisée
3. FLD-NEIGHBORHOOD — Secteur précis
4. FLD-ACCESSIBILITE — Accès au terrain

### next_question
"Un terrain en zone rurale près de Mbalmayo pour l'agriculture. Quelle surface minimum et quel budget maximum ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander surface et budget
- Préciser le secteur
- Discuter de l'accès

### forbidden_actions
- Proposer des terrains en zone urbaine
- Ignorer la destination agricole

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-USAGE: hard_constraint + weight 25
- FLD-ZONE: hard_constraint + weight 20

---

## SCENARIO-038: Terrain à morceler

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_non_titre
- **transaction_type**: BUY
- **requester_profile**: promoteur

### initial_message
"Je cherche un grand terrain à Douala pour le morceler et revendre. Minimum 1000 m²."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_non_titre
- FLD-CITY: Douala
- FLD-SURFACE_MIN: 1000
- FLD-USAGE: INVESTISSEMENT_MORCELLEMENT

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-NEIGHBORHOOD — Quartier non mentionné
3. FLD-DOCUMENT — Type de document attendu
4. FLD-DISPONIBILITE — Délai

### next_question
"Un grand terrain de 1000 m² minimum à Douala pour morceler. Quel budget et dans quel secteur ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander budget et secteur
- Discuter des aspects légaux du morcellement
- Proposer des professionnels (géomètre)

### forbidden_actions
- Proposer des terrains trop petits
- Ignorer les aspects réglementaires

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-SURFACE_MIN: hard_constraint + weight 25
- FLD-USAGE: hard_constraint + weight 20

---

## Scenarios 39-44: Land — Other

## SCENARIO-039: Parcelle résidentielle

### context
- **request_family**: LAND_SEARCH
- **property_type**: parcelle_residentielle
- **transaction_type**: BUY
- **requester_profile**: particulier

### initial_message
"Je cherche une parcelle résidentielle à Limbé pour construire une petite maison de vacances."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: parcelle_residentielle
- FLD-CITY: Limbé
- FLD-USAGE: RESIDENCE_VACANCES

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE — Surface non précisée
3. FLD-NEIGHBORHOOD — Quartier non mentionné
4. FLD-DOCUMENT — Type de document

### next_question
"Une parcelle résidentielle à Limbé pour une maison de vacances. Quelle surface minimum et quel budget ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander surface et budget
- Préciser le secteur à Limbé
- Discuter de la proximité mer

### forbidden_actions
- Proposer des parcelles non résidentielles
- Ignorer la localisation Limbé

### matching_criteria
- FLD-CITY: hard_constraint + weight 30
- FLD-PROPERTY_TYPE: hard_constraint + weight 25

---

## SCENARIO-040: Terrain agricole

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_agricole
- **transaction_type**: BUY
- **requester_profile**: agriculteur

### initial_message
"Je cherche un terrain agricole d'au moins 2 hectares à Foumban pour cultiver."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_agricole
- FLD-CITY: Foumban
- FLD-SURFACE_MIN: 20000
- FLD-USAGE: AGRICOLE

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-NEIGHBORHOOD — Zone précise
3. FLD-DOCUMENT — Type de document
4. FLD-ACCESSIBILITE — Accès au terrain
5. FLD-EAU — Disponibilité en eau

### next_question
"Un terrain agricole de 2 hectares à Foumban. Quel budget maximum et dans quelle zone exactement ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander budget
- Préciser la zone
- Discuter de l'accès à l'eau

### forbidden_actions
- Proposer des terrains non agricoles
- Ignorer la taille minimum

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-SURFACE_MIN: hard_constraint + weight 25
- FLD-USAGE: hard_constraint + weight 25

---

## SCENARIO-041: Terrain commercial

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_commercial
- **transaction_type**: BUY
- **requester_profile**: commerçant

### initial_message
"Je cherche un terrain commercial à Douala en bordure de route, pour construire un magasin."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_commercial
- FLD-CITY: Douala
- FLD-USAGE: COMMERCIAL
- FLD-VISIBILITE: ROUTE_PRINCIPALE

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE — Surface non précisée
3. FLD-NEIGHBORHOOD — Quartier non mentionné
4. FLD-DOCUMENT — Type de document

### next_question
"Un terrain commercial en bordure de route à Douala. Quel budget et dans quel quartier ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander budget et quartier
- Noter l'exigence de visibilité
- Discuter du flux routier

### forbidden_actions
- Proposer des terrains sans accès route
- Ignorer le caractère commercial

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 25
- FLD-USAGE: hard_constraint + weight 20

---

## SCENARIO-042: Domaine rural

### context
- **request_family**: LAND_SEARCH
- **property_type**: domaine_rural
- **transaction_type**: BUY
- **requester_profile**: investisseur

### initial_message
"Je cherche un domaine rural à vendre dans le Centre, pour un projet écotouristique."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: domaine_rural
- FLD-REGION: Centre
- FLD-USAGE: ECOTOURISME

### missing_fields (ordered by priority)
1. FLD-CITY — Ville précise non mentionnée
2. FLD-BUDGET_MAX — Budget non mentionné
3. FLD-SURFACE — Surface non précisée
4. FLD-DOCUMENT — Type de document

### next_question
"Un domaine rural dans la région du Centre pour l'écotourisme. Dans quelle ville précisément et quelle surface ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander ville et surface
- Discuter du projet écotouristique
- Vérifier les documents nécessaires

### forbidden_actions
- Proposer des terrains sans potentiel touristique
- Ignorer la réglementation spécifique

### matching_criteria
- FLD-REGION: hard_constraint + weight 25
- FLD-USAGE: hard_constraint + weight 25

---

## SCENARIO-043: Concession

### context
- **request_family**: LAND_SEARCH
- **property_type**: concession
- **transaction_type**: BUY
- **requester_profile**: famille élargie

### initial_message
"Nous cherchons une concession familiale à vendre à Yaoundé, avec plusieurs bâtiments, pour notre grande famille."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: concession
- FLD-CITY: Yaoundé
- FLD-USAGE: FAMILIAL

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE — Surface non précisée
3. FLD-NEIGHBORHOOD — Quartier non mentionné
4. FLD-NOMBRE_BATIMENTS — Nombre de bâtiments
5. FLD-DOCUMENT — Type de document

### next_question
"Une concession familiale à Yaoundé. Quelle surface totale et quel budget maximum ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander surface et budget
- Préciser le nombre de bâtiments
- Discuter du quartier

### forbidden_actions
- Proposer des propriétés trop petites
- Ignorer le caractère familial

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 25

---

## SCENARIO-044: Terrain pour investissement

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_titre
- **transaction_type**: BUY
- **requester_profile**: investisseur

### initial_message
"Je cherche un terrain à acheter comme investissement à Douala, dans une zone qui va prendre de la valeur."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_titre
- FLD-CITY: Douala
- FLD-USAGE: INVESTISSEMENT

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE — Surface non précisée
3. FLD-NEIGHBORHOOD — Quartier à potentiel
4. FLD-DELAI — Horizon d'investissement
5. FLD-DOCUMENT — Type de document

### next_question
"Un terrain pour investissement à Douala. Quel budget et dans quel secteur voyez-vous du potentiel ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander budget et secteurs d'intérêt
- Conseiller sur les zones à potentiel
- Discuter de la stratégie d'investissement

### forbidden_actions
- Proposer des terrains sans potentiel de valorisation
- Donner des conseils financiers sans précaution

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 20
- FLD-USAGE: hard_constraint + weight 25

---

## Scenarios 45-52: Commercial

## SCENARIO-045: Local commercial pour boutique

### context
- **request_family**: COMMERCIAL_SEARCH
- **property_type**: boutique
- **transaction_type**: RENT
- **requester_profile**: commerçant

### initial_message
"Bonjour, je cherche un local commercial pour boutique de vêtements à Douala, Bonanjo, max 500 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: boutique
- FLD-CITY: Douala
- FLD-NEIGHBORHOOD: Bonanjo
- FLD-BUDGET_MAX: 500000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-ACTIVITE: VETEMENTS

### missing_fields (ordered by priority)
1. FLD-SURFACE_MIN — Surface de vente
2. FLD-DISPONIBILITE — Disponibilité
3. FLD-VISIBILITE — Visibilité souhaitée
4. FLD-DUREE_BAIL — Durée du bail

### next_question
"Une boutique de vêtements à Bonanjo, Douala pour 500 000 FCFA. Quelle surface de vente minimum vous faut-il ?"

### readiness_level
MINIMUM_SEARCH_READY

### allowed_actions
- Lancer la recherche
- Filtrer boutiques à Bonanjo
- Demander précisions surface

### forbidden_actions
- Proposer des locaux non commerciaux
- Ignorer le type d'activité

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-NEIGHBORHOOD: hard_constraint + weight 20
- FLD-BUDGET_MAX: hard_constraint + weight 15
- FLD-ACTIVITE: hard_constraint + weight 15

---

## SCENARIO-046: Bureau en location

### context
- **request_family**: COMMERCIAL_SEARCH
- **property_type**: bureau
- **transaction_type**: RENT
- **requester_profile**: professionnel libéral

### initial_message
"Je cherche un bureau meublé à Yaoundé, centre-ville, pour mon cabinet comptable, max 300 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: bureau
- FLD-CITY: Yaoundé
- FLD-ZONE: centre-ville
- FLD-BUDGET_MAX: 300000
- FLD-BUDGET_TYPE: MONTHLY_RENT
- FLD-MEUBLE: OUI

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier précis
2. FLD-SURFACE_MIN — Surface minimum
3. FLD-DISPONIBILITE — Disponibilité
4. FLD-PARKING — Parking client

### next_question
"Un bureau meublé au centre-ville de Yaoundé pour 300 000 FCFA. Dans quel quartier exactement ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander le quartier précis
- Confirmer le besoin meublé
- Vérifier la surface

### forbidden_actions
- Proposer des bureaux non meublés
- Ignorer la localisation centre-ville

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-PROPERTY_TYPE: hard_constraint + weight 20

---

## SCENARIO-047: Entrepôt avec accès poids lourds

### context
- **request_family**: COMMERCIAL_SEARCH
- **property_type**: entrepot
- **transaction_type**: RENT
- **requester_profile**: logisticien

### initial_message
"Je cherche un entrepôt à Douala avec accès pour poids lourds, zone industrielle, minimum 500 m²."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: entrepot
- FLD-CITY: Douala
- FLD-ZONE: zone industrielle
- FLD-SURFACE_MIN: 500
- FLD-ACCES_POIDS_LOURDS: OUI

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-NEIGHBORHOOD — Quartier industriel précis
3. FLD-DISPONIBILITE — Disponibilité
4. FLD-HAUTEUR_SOUS_PLAFOND — Hauteur requise
5. FLD-ELECTRICITE — Type d'alimentation

### next_question
"Un entrepôt de 500 m² avec accès poids lourds en zone industrielle à Douala. Quel budget maximum ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander le budget
- Préciser la zone industrielle
- Discuter des besoins logistiques

### forbidden_actions
- Proposer des locaux sans accès poids lourds
- Proposer en zone non industrielle

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-SURFACE_MIN: hard_constraint + weight 25
- FLD-ACCES_POIDS_LOURDS: hard_constraint + weight 25

---

## SCENARIO-048: Restaurant activité restauration

### context
- **request_family**: COMMERCIAL_SEARCH
- **property_type**: local_commercial
- **transaction_type**: RENT
- **requester_profile**: restaurateur

### initial_message
"Bonjour, je cherche un local pour ouvrir un restaurant à Yaoundé, côté Bastos, avec une belle terrasse."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: local_commercial
- FLD-CITY: Yaoundé
- FLD-NEIGHBORHOOD: Bastos
- FLD-ACTIVITE: RESTAURATION
- FLD-TERRASSE: OUI

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE_MIN — Surface minimum
3. FLD-DISPONIBILITE — Disponibilité
4. FLD-EQUIPEMENT_CUISINE — Cuisine existante ?
5. FLD-NORME_HYGIENE — Normes requises

### next_question
"Un local pour restaurant avec terrasse à Bastos, Yaoundé. Quelle surface minimum et quel budget maximum ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander surface et budget
- Noter le besoin terrasse
- Discuter des équipements

### forbidden_actions
- Proposer des locaux sans terrasse
- Ignorer les normes restauration

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-NEIGHBORHOOD: hard_constraint + weight 20
- FLD-ACTIVITE: hard_constraint + weight 25

---

## SCENARIO-049: Magasin avec visibilité route

### context
- **request_family**: COMMERCIAL_SEARCH
- **property_type**: magasin
- **transaction_type**: RENT
- **requester_profile**: commerçant

### initial_message
"Je cherche un magasin avec une bonne visibilité sur la route principale à Douala, pour vendre des meubles."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: magasin
- FLD-CITY: Douala
- FLD-VISIBILITE: ROUTE_PRINCIPALE
- FLD-ACTIVITE: MEUBLES

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE_MIN — Surface de vente
3. FLD-NEIGHBORHOOD — Quartier non mentionné
4. FLD-PARKING — Parking clients
5. FLD-DISPONIBILITE — Disponibilité

### next_question
"Un magasin sur route principale à Douala pour vendre des meubles. Dans quel quartier et quel budget ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander quartier et budget
- Noter l'exigence de visibilité
- Discuter de la surface d'exposition

### forbidden_actions
- Proposer des magasins sans visibilité route
- Proposer en zones secondaires

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-VISIBILITE: hard_constraint + weight 25
- FLD-ACTIVITE: hard_constraint + weight 20

---

## SCENARIO-050: Hôtel ou auberge

### context
- **request_family**: COMMERCIAL_SEARCH
- **property_type**: hotel
- **transaction_type**: BUY
- **requester_profile**: investisseur hôtelier

### initial_message
"Je cherche un hôtel ou une auberge à vendre à Kribi, proche de la plage, pour investissement."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: hotel
- FLD-CITY: Kribi
- FLD-PROXIMITE: PLAGE
- FLD-USAGE: INVESTISSEMENT

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-NOMBRE_CHAMBRES — Nombre de chambres
3. FLD-NEIGHBORHOOD — Secteur précis
4. FLD-SURFACE_TERRAIN — Surface terrain
5. FLD-NORME_CLASSIFICATION — Classification

### next_question
"Un hôtel ou auberge près de la plage à Kribi. Quel budget maximum et combien de chambres minimum ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander budget et nombre de chambres
- Discuter du potentiel touristique
- Vérifier la classification

### forbidden_actions
- Proposer des propriétés loin de la plage
- Ignorer le caractère hôtelier

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 25
- FLD-PROXIMITE: hard_constraint + weight 20

---

## SCENARIO-051: Immeuble de rapport

### context
- **request_family**: COMMERCIAL_SEARCH
- **property_type**: immeuble_rapport
- **transaction_type**: BUY
- **requester_profile**: investisseur

### initial_message
"Je cherche un immeuble de rapport à acheter à Douala, avec au moins 6 appartements, budget 150 millions."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: immeuble_rapport
- FLD-CITY: Douala
- FLD-BUDGET_MAX: 150000000
- FLD-BUDGET_TYPE: TOTAL_PRICE
- FLD-NOMBRE_LOGEMENTS: 6

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-RENDEMENT_ATTENDU — Rendement locatif attendu
3. FLD-DISPONIBILITE — Délai d'achat
4. FLD-ETAT_BATIMENT — État du bâtiment

### next_question
"Un immeuble de rapport d'au moins 6 appartements à Douala pour 150 millions. Dans quel quartier ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander le quartier
- Discuter du rendement attendu
- Proposer une estimation

### forbidden_actions
- Proposer des immeubles avec moins de 6 logements
- Ignorer l'aspect investissement

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-NOMBRE_LOGEMENTS: hard_constraint + weight 20

---

## SCENARIO-052: Station-service

### context
- **request_family**: COMMERCIAL_SEARCH
- **property_type**: station_service
- **transaction_type**: BUY
- **requester_profile**: investisseur

### initial_message
"Je cherche une station-service à vendre sur l'axe Douala-Yaoundé, avec toutes les licences."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: station_service
- FLD-LOCALISATION: Axe Douala-Yaoundé
- FLD-LICENCES: OUI

### missing_fields (ordered by priority)
1. FLD-CITY — Ville la plus proche
2. FLD-BUDGET_MAX — Budget non mentionné
3. FLD-SURFACE_TERRAIN — Surface terrain
4. FLD-DISPONIBILITE — Délai d'achat
5. FLD-EQUIPEMENTS — Équipements (citerne, pompes, etc.)

### next_question
"Une station-service avec licences sur l'axe Douala-Yaoundé. Quel budget maximum et près de quelle ville exactement ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander budget et ville précise
- Vérifier les licences
- Discuter des équipements

### forbidden_actions
- Proposer des stations sans licence
- Ignorer les aspects réglementaires

### matching_criteria
- FLD-PROPERTY_TYPE: hard_constraint + weight 30
- FLD-LICENCES: hard_constraint + weight 25

---

## Scenarios 53-58: Financing

## SCENARIO-053: Crédit immobilier salarié

### context
- **request_family**: FINANCING_REQUEST
- **property_type**: FINANCING
- **transaction_type**: FINANCE
- **requester_profile**: salarié

### initial_message
"Bonjour, je suis fonctionnaire et je veux un crédit immobilier pour acheter un appartement à Yaoundé."

### extracted_facts
- FLD-OBJET_FINANCEMENT: credit_immobilier
- FLD-PROFIL_DEMANDEUR: SALARIE
- FLD-TYPE_BIEN_PROJET: appartement_non_meuble
- FLD-TRANSACTION: BUY
- FLD-CITY: Yaoundé

### missing_fields (ordered by priority)
1. FLD-MONTANT_RECHERCHE — Montant du prêt souhaité
2. FLD-APPORT — Apport personnel disponible
3. FLD-REVENUS — Revenus mensuels
4. FLD-DUREE_SOUHAITEE — Durée du crédit
5. FLD-EMPLOYEUR — Employeur précis

### next_question
"Bonjour ! Un crédit immobilier pour un appartement à Yaoundé. Quel montant souhaitez-vous emprunter et quel apport pouvez-vous apporter ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Confirmer le besoin de financement
- Demander montant et apport
- Discuter du profil salarié

### forbidden_actions
- Proposer des biens sans financement
- Demander des documents trop tôt

### matching_criteria
- FLD-OBJET_FINANCEMENT: hard_constraint + weight 30
- FLD-PROFIL_DEMANDEUR: hard_constraint + weight 25

---

## SCENARIO-054: Financement construction

### context
- **request_family**: FINANCING_REQUEST
- **property_type**: FINANCING
- **transaction_type**: FINANCE
- **requester_profile**: particulier

### initial_message
"Salut, j'ai un terrain à Douala et je veux un prêt pour construire ma maison."

### extracted_facts
- FLD-OBJET_FINANCEMENT: credit_construction
- FLD-TERRAIN_DISPONIBLE: OUI
- FLD-CITY: Douala

### missing_fields (ordered by priority)
1. FLD-MONTANT_RECHERCHE — Montant du prêt
2. FLD-APPORT — Apport personnel
3. FLD-COUT_TOTAL_PROJET — Coût total construction
4. FLD-REVENUS — Revenus mensuels
5. FLD-PROFIL_DEMANDEUR — Profil emprunteur

### next_question
"Vous avez un terrain à Douala et voulez un prêt construction. Combien coûte votre projet et quel apport pouvez-vous mettre ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Confirmer le projet construction
- Demander coût et apport
- Discuter du planning

### forbidden_actions
- Proposer des crédits sans terrain
- Ignorer le coût total du projet

### matching_criteria
- FLD-OBJET_FINANCEMENT: hard_constraint + weight 30
- FLD-TERRAIN_DISPONIBLE: hard_constraint + weight 20

---

## SCENARIO-055: Financement acquisition terrain

### context
- **request_family**: FINANCING_REQUEST
- **property_type**: FINANCING
- **transaction_type**: FINANCE
- **requester_profile**: jeune actif

### initial_message
"Je veux acheter un terrain à Bafoussam mais j'ai besoin d'un financement, j'ai 500 000 d'apport."

### extracted_facts
- FLD-OBJET_FINANCEMENT: credit_acquisition_terrain
- FLD-CITY: Bafoussam
- FLD-APPORT: 500000

### missing_fields (ordered by priority)
1. FLD-MONTANT_RECHERCHE — Montant à emprunter
2. FLD-PRIX_TERRAIN — Prix du terrain visé
3. FLD-REVENUS — Revenus mensuels
4. FLD-PROFIL_DEMANDEUR — Profil emprunteur
5. FLD-SOURCE_FINANCEMENT — Source du financement

### next_question
"Un financement pour terrain à Bafoussam avec 500 000 FCFA d'apport. Quel est le prix du terrain et combien souhaitez-vous emprunter ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Confirmer l'acquisition terrain
- Demander montant et prix
- Évaluer le rapport apport/montant

### forbidden_actions
- Proposer des options sans connaître le prix
- Ignorer le besoin d'apport complémentaire

### matching_criteria
- FLD-OBJET_FINANCEMENT: hard_constraint + weight 30
- FLD-APPORT: soft_constraint + weight 25

---

## SCENARIO-056: Recherche investisseur projet

### context
- **request_family**: FINANCING_REQUEST
- **property_type**: FINANCING
- **transaction_type**: FINANCE
- **requester_profile**: promoteur

### initial_message
"Je cherche un investisseur pour financer mon projet de construction de 8 appartements à Douala."

### extracted_facts
- FLD-OBJET_FINANCEMENT: recherche_investisseur
- FLD-TYPE_PROJET: construction_appartements
- FLD-NOMBRE_LOGEMENTS: 8
- FLD-CITY: Douala

### missing_fields (ordered by priority)
1. FLD-MONTANT_RECHERCHE — Montant nécessaire
2. FLD-APPORT — Apport du promoteur
3. FLD-COUT_TOTAL_PROJET — Coût total
4. FLD-DOCUMENTS_PROJET — Business plan, permis
5. FLD-DELAI — Délai du projet

### next_question
"Un projet de 8 appartements à Douala cherche un investisseur. Quel est le budget total du projet et combien cherchez-vous ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander les détails du projet
- Vérifier la viabilité
- Proposer une mise en relation

### forbidden_actions
- Promettre un financement garanti
- Ignorer les documents du projet

### matching_criteria
- FLD-OBJET_FINANCEMENT: hard_constraint + weight 30
- FLD-CITY: hard_constraint + weight 20

---

## SCENARIO-057: Microfinance pour rénovation

### context
- **request_family**: FINANCING_REQUEST
- **property_type**: FINANCING
- **transaction_type**: FINANCE
- **requester_profile**: petit commerçant

### initial_message
"Bonjour, je veux un petit crédit pour rénover ma boutique à Douala, environ 2 millions."

### extracted_facts
- FLD-OBJET_FINANCEMENT: microfinance_renovation
- FLD-MONTANT_RECHERCHE: 2000000
- FLD-CITY: Douala
- FLD-TYPE_BIEN_PROJET: boutique

### missing_fields (ordered by priority)
1. FLD-APPORT — Apport disponible
2. FLD-REVENUS — Revenus mensuels
3. FLD-PROFIL_DEMANDEUR — Profil emprunteur
4. FLD-GARANTIES — Garanties disponibles
5. FLD-DUREE_SOUHAITEE — Durée du prêt

### next_question
"Un crédit de 2 millions pour rénover votre boutique à Douala. Quel apport pouvez-vous apporter et quels sont vos revenus mensuels ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer le montant
- Demander apport et revenus
- Discuter des garanties

### forbidden_actions
- Proposer des montants supérieurs
- Ignorer la capacité de remboursement

### matching_criteria
- FLD-OBJET_FINANCEMENT: hard_constraint + weight 25
- FLD-MONTANT_RECHERCHE: hard_constraint + weight 25

---

## SCENARIO-058: Diaspora financement apport

### context
- **request_family**: FINANCING_REQUEST
- **property_type**: FINANCING
- **transaction_type**: FINANCE
- **requester_profile**: diaspora

### initial_message
"Je suis camerounais vivant en France, je veux acheter un terrain à Yaoundé et j'ai besoin d'un crédit pour compléter."

### extracted_facts
- FLD-OBJET_FINANCEMENT: credit_acquisition_terrain
- FLD-DIASPORA: OUI
- FLD-PAYS_RESIDENCE: France
- FLD-CITY: Yaoundé

### missing_fields (ordered by priority)
1. FLD-MONTANT_RECHERCHE — Montant à emprunter
2. FLD-APPORT — Apport disponible
3. FLD-REVENUS — Revenus en France
4. FLD-PROFIL_DEMANDEUR — Profil (salarié en France)
5. FLD-JUSTIFICATIFS_REVENUS — Justificatifs spécifiques diaspora

### next_question
"Bonjour ! Un crédit pour terrain à Yaoundé depuis la France. Quel est le prix du terrain visé et quel apport avez-vous ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Confirmer le statut diaspora
- Demander montant et apport
- Proposer des solutions adaptées diaspora

### forbidden_actions
- Proposer des solutions standard sans adaptation diaspora
- Ignorer les spécificités des revenus en devise

### matching_criteria
- FLD-OBJET_FINANCEMENT: hard_constraint + weight 25
- FLD-DIASPORA: ranking_preference + weight 25

---

## Scenarios 59-66: Professional

## SCENARIO-059: Recherche architecte construction

### context
- **request_family**: PROFESSIONAL_SEARCH
- **property_type**: PROFESSIONAL
- **transaction_type**: FIND
- **requester_profile**: particulier

### initial_message
"Bonjour, je cherche un architecte à Yaoundé pour les plans de ma villa."

### extracted_facts
- FLD-TYPE_PRESTATION: recherche_professionnel
- FLD-PROFESSION_TYPE: architecte
- FLD-CITY: Yaoundé
- FLD-DESCRIPTION_BESOIN: plans villa

### missing_fields (ordered by priority)
1. FLD-SURFACE_PROJET — Surface de la villa
2. FLD-DELAI — Délai du projet
3. FLD-BUDGET_HONORAIRES — Budget honoraires
4. FLD-DISPONIBILITE — Disponibilité

### next_question
"Un architecte à Yaoundé pour les plans de votre villa. Quelle surface et quel est votre budget pour les honoraires ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander les précisions du projet
- Proposer des architectes partenaires
- Discuter du budget

### forbidden_actions
- Proposer d'autres professionnels sans confirmation
- Négliger les détails du projet

### matching_criteria
- FLD-PROFESSION_TYPE: hard_constraint + weight 30
- FLD-CITY: hard_constraint + weight 25

---

## SCENARIO-060: Recherche notaire pour achat

### context
- **request_family**: PROFESSIONAL_SEARCH
- **property_type**: PROFESSIONAL
- **transaction_type**: FIND
- **requester_profile**: acheteur

### initial_message
"Je suis sur le point d'acheter un terrain à Douala, je cherche un notaire pour m'accompagner."

### extracted_facts
- FLD-TYPE_PRESTATION: recherche_professionnel
- FLD-PROFESSION_TYPE: notaire
- FLD-CITY: Douala
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_titre

### missing_fields (ordered by priority)
1. FLD-DELAI_SOUHAITE — Date de la transaction
2. FLD-BUDGET_HONORAIRES — Budget
3. FLD-DISPONIBILITE — Disponibilité pour rencontrer

### next_question
"Un notaire pour l'achat de votre terrain à Douala. Quand comptez-vous finaliser la transaction ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Confirmer le besoin de notaire
- Proposer des notaires partenaires
- Discuter des frais

### forbidden_actions
- Proposer des professionnels non notaires
- Négliger les spécificités du terrain

### matching_criteria
- FLD-PROFESSION_TYPE: hard_constraint + weight 35
- FLD-CITY: hard_constraint + weight 25

---

## SCENARIO-061: Recherche géomètre pour bornage

### context
- **request_family**: PROFESSIONAL_SEARCH
- **property_type**: PROFESSIONAL
- **transaction_type**: FIND
- **requester_profile**: propriétaire

### initial_message
"Bonjour, j'ai besoin d'un géomètre à Bafoussam pour le bornage de mon terrain."

### extracted_facts
- FLD-TYPE_PRESTATION: recherche_professionnel
- FLD-PROFESSION_TYPE: geometre
- FLD-CITY: Bafoussam
- FLD-DESCRIPTION_BESOIN: bornage terrain

### missing_fields (ordered by priority)
1. FLD-SURFACE_TERRAIN — Surface du terrain
2. FLD-DISPONIBILITE — Disponibilité
3. FLD-URGENCE — Degré d'urgence
4. FLD-DOCUMENTS_DISPONIBLES — Documents existants

### next_question
"Un géomètre pour bornage à Bafoussam. Quelle est la surface de votre terrain et quand souhaitez-vous faire le bornage ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander les détails du terrain
- Proposer des géomètres partenaires
- Discuter du processus

### forbidden_actions
- Proposer d'autres professionnels
- Ignorer l'urgence éventuelle

### matching_criteria
- FLD-PROFESSION_TYPE: hard_constraint + weight 35
- FLD-CITY: hard_constraint + weight 25

---

## SCENARIO-062: Recherche agent immobilier vente

### context
- **request_family**: PROFESSIONAL_SEARCH
- **property_type**: PROFESSIONAL
- **transaction_type**: SELL
- **requester_profile**: vendeur

### initial_message
"Je veux vendre ma villa à Douala, je cherche un agent immobilier professionnel."

### extracted_facts
- FLD-TYPE_PRESTATION: recherche_professionnel
- FLD-PROFESSION_TYPE: agent_immobilier
- FLD-CITY: Douala
- FLD-TRANSACTION: SELL
- FLD-PROPERTY_TYPE: villa

### missing_fields (ordered by priority)
1. FLD-PRIX_VENTE — Prix de vente souhaité
2. FLD-DELAI_VENTE — Délai de vente
3. FLD-MANDAT_TYPE — Type de mandat souhaité
4. FLD-DISPONIBILITE — Disponibilité

### next_question
"Un agent immobilier pour vendre votre villa à Douala. À quel prix souhaitez-vous vendre et dans quel délai ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Confirmer la vente
- Demander prix et délai
- Proposer des agents spécialisés

### forbidden_actions
- Proposer des agents non professionnels
- Négliger le type de mandat

### matching_criteria
- FLD-PROFESSION_TYPE: hard_constraint + weight 30
- FLD-CITY: hard_constraint + weight 20
- FLD-PROPERTY_TYPE: hard_constraint + weight 20

---

## SCENARIO-063: Recherche maçon pour travaux

### context
- **request_family**: PROFESSIONAL_SEARCH
- **property_type**: PROFESSIONAL
- **transaction_type**: FIND
- **requester_profile**: particulier

### initial_message
"Je cherche un maçon à Douala pour construire un mur de clôture et une petite extension."

### extracted_facts
- FLD-TYPE_PRESTATION: recherche_professionnel
- FLD-PROFESSION_TYPE: macon
- FLD-CITY: Douala
- FLD-DESCRIPTION_BESOIN: mur cloture + extension

### missing_fields (ordered by priority)
1. FLD-DISPONIBILITE — Disponibilité
2. FLD-DELAI — Délai des travaux
3. FLD-BUDGET_TRAVAUX — Budget des travaux
4. FLD-URGENCE — Degré d'urgence
5. FLD-MATERIAUX — Matériaux (fournis par client ou entreprise)

### next_question
"Un maçon à Douala pour mur de clôture et extension. Quel est votre budget et quand voulez-vous commencer ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander budget et délai
- Proposer des maçons partenaires
- Discuter des matériaux

### forbidden_actions
- Proposer des professionnels non qualifiés
- Ignorer le périmètre des travaux

### matching_criteria
- FLD-PROFESSION_TYPE: hard_constraint + weight 35
- FLD-CITY: hard_constraint + weight 25

---

## SCENARIO-064: Recherche électricien

### context
- **request_family**: PROFESSIONAL_SEARCH
- **property_type**: PROFESSIONAL
- **transaction_type**: FIND
- **requester_profile**: particulier

### initial_message
"Bonjour, j'ai des problèmes d'électricité dans mon appartement, je cherche un bon électricien à Yaoundé."

### extracted_facts
- FLD-TYPE_PRESTATION: recherche_professionnel
- FLD-PROFESSION_TYPE: electricien
- FLD-CITY: Yaoundé
- FLD-DESCRIPTION_BESOIN: dépannage électrique

### missing_fields (ordered by priority)
1. FLD-DISPONIBILITE — Disponibilité
2. FLD-URGENCE — Degré d'urgence (panne)
3. FLD-TYPE_TRAVAUX — Type : dépannage ou installation
4. FLD-DELAI — Délai souhaité

### next_question
"Un électricien à Yaoundé pour dépannage. C'est urgent ? Quand souhaitez-vous qu'il passe ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander le degré d'urgence
- Proposer des électriciens disponibles
- Discuter du type d'intervention

### forbidden_actions
- Proposer des professionnels non électriciens
- Ignorer l'urgence

### matching_criteria
- FLD-PROFESSION_TYPE: hard_constraint + weight 35
- FLD-CITY: hard_constraint + weight 25

---

## SCENARIO-065: Recherche photographe immobilier

### context
- **request_family**: PROFESSIONAL_SEARCH
- **property_type**: PROFESSIONAL
- **transaction_type**: FIND
- **requester_profile**: agent immobilier

### initial_message
"Je suis agent immobilier et je cherche un photographe pro pour shooter mes biens à Douala."

### extracted_facts
- FLD-TYPE_PRESTATION: recherche_professionnel
- FLD-PROFESSION_TYPE: photographe_immobilier
- FLD-CITY: Douala
- FLD-PROFIL_DEMANDEUR: agent_immobilier

### missing_fields (ordered by priority)
1. FLD-NOMBRE_BIENS — Nombre de biens à shooter
2. FLD-DISPONIBILITE — Disponibilité
3. FLD-BUDGET — Budget par séance
4. FLD-DELAI — Délai

### next_question
"Un photographe immobilier à Douala pour vos biens. Combien de biens à shooter et quel est votre budget ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander le nombre de biens
- Proposer des photographes partenaires
- Discuter des tarifs

### forbidden_actions
- Proposer des photographes non spécialisés immobilier
- Ignorer le volume de travail

### matching_criteria
- FLD-PROFESSION_TYPE: hard_constraint + weight 35
- FLD-CITY: hard_constraint + weight 25

---

## SCENARIO-066: Recherche expert immobilier

### context
- **request_family**: PROFESSIONAL_SEARCH
- **property_type**: PROFESSIONAL
- **transaction_type**: FIND
- **requester_profile**: investisseur

### initial_message
"Je cherche un expert immobilier pour évaluer un immeuble que je veux acheter à Douala."

### extracted_facts
- FLD-TYPE_PRESTATION: recherche_professionnel
- FLD-PROFESSION_TYPE: expert_immobilier
- FLD-CITY: Douala
- FLD-DESCRIPTION_BESOIN: évaluation immeuble
- FLD-TRANSACTION: BUY

### missing_fields (ordered by priority)
1. FLD-TYPE_BIEN — Type de bien à évaluer
2. FLD-DISPONIBILITE — Disponibilité
3. FLD-DELAI — Délai de l'expertise
4. FLD-BUDGET — Budget expertise

### next_question
"Un expert pour évaluer un immeuble à Douala. De quel type d'immeuble s'agit-il et quand avez-vous besoin de l'expertise ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander le type d'immeuble
- Proposer des experts partenaires
- Discuter du processus d'évaluation

### forbidden_actions
- Proposer des professionnels non experts
- Donner une estimation sans expertise

### matching_criteria
- FLD-PROFESSION_TYPE: hard_constraint + weight 35
- FLD-CITY: hard_constraint + weight 25

---

## Scenarios 67-74: Services

## SCENARIO-067: Demande estimation immobilière

### context
- **request_family**: REAL_ESTATE_SERVICE
- **property_type**: SERVICE
- **transaction_type**: SERVICE
- **requester_profile**: propriétaire

### initial_message
"Bonjour, je voudrais une estimation de ma villa à Yaoundé, Bastos, 4 chambres."

### extracted_facts
- FLD-SERVICE_TYPE: estimation_immobiliere
- FLD-PROPERTY_TYPE: villa
- FLD-CITY: Yaoundé
- FLD-NEIGHBORHOOD: Bastos
- FLD-CHAMBRES: 4

### missing_fields (ordered by priority)
1. FLD-SURFACE — Surface habitable
2. FLD-ETAT — État du bien
3. FLD-TRANSACTION — Vente ou location ?
4. FLD-DISPONIBILITE — Disponibilité pour visite

### next_question
"Une estimation pour votre villa 4 chambres à Bastos, Yaoundé. C'est pour une vente ou une location ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander le but de l'estimation
- Préciser les caractéristiques
- Proposer une visite d'estimation

### forbidden_actions
- Donner une estimation sans visite
- Ignorer l'état du bien

### matching_criteria
- FLD-SERVICE_TYPE: hard_constraint + weight 30
- FLD-CITY: hard_constraint + weight 20

---

## SCENARIO-068: Demande gestion locative

### context
- **request_family**: REAL_ESTATE_SERVICE
- **property_type**: SERVICE
- **transaction_type**: SERVICE
- **requester_profile**: bailleur

### initial_message
"Bonjour, je cherche une agence pour gérer mes 3 appartements en location à Douala."

### extracted_facts
- FLD-SERVICE_TYPE: gestion_locative
- FLD-CITY: Douala
- FLD-NOMBRE_BIENS: 3
- FLD-PROPERTY_TYPE: appartement_non_meuble

### missing_fields (ordered by priority)
1. FLD-LOYER_MENSUEL — Loyer mensuel par bien
2. FLD-DISPONIBILITE — Disponibilité pour mandat
3. FLD-LOCATAIRES_EXISTANTS — Locataires en place ?
4. FLD-MANDAT_TYPE — Type de mandat souhaité

### next_question
"La gestion de vos 3 appartements à Douala. Sont-ils actuellement loués et quel est le loyer mensuel de chaque bien ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander les détails des biens
- Discuter des services de gestion
- Proposer une convention de mandat

### forbidden_actions
- Proposer des services non adaptés
- Ignorer les locataires existants

### matching_criteria
- FLD-SERVICE_TYPE: hard_constraint + weight 30
- FLD-CITY: hard_constraint + weight 20

---

## SCENARIO-069: Demande home staging

### context
- **request_family**: REAL_ESTATE_SERVICE
- **property_type**: SERVICE
- **transaction_type**: SERVICE
- **requester_profile**: vendeur

### initial_message
"Je veux vendre mon appartement mais il est vide, je cherche quelqu'un pour le home staging à Douala."

### extracted_facts
- FLD-SERVICE_TYPE: home_staging
- FLD-CITY: Douala
- FLD-TRANSACTION: SELL
- FLD-PROPERTY_TYPE: appartement_meuble
- FLD-ETAT: VIDE

### missing_fields (ordered by priority)
1. FLD-SURFACE — Surface à meubler/stager
2. FLD-PIECES — Nombre de pièces
3. FLD-BUDGET — Budget home staging
4. FLD-DELAI — Délai avant mise en vente
5. FLD-STYLE_PREFERE — Style de décoration

### next_question
"Un home staging pour votre appartement vide à Douala. Combien de pièces et quel est votre budget pour le staging ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander surface et budget
- Proposer des home stagers partenaires
- Discuter du style

### forbidden_actions
- Proposer des services sans connaître le bien
- Ignorer le délai de vente

### matching_criteria
- FLD-SERVICE_TYPE: hard_constraint + weight 30
- FLD-CITY: hard_constraint + weight 20

---

## SCENARIO-070: Demande vérification documentaire

### context
- **request_family**: REAL_ESTATE_SERVICE
- **property_type**: SERVICE
- **transaction_type**: SERVICE
- **requester_profile**: acheteur

### initial_message
"Bonjour, je veux acheter un terrain mais j'ai des doutes sur les papiers, je cherche quelqu'un pour vérifier."

### extracted_facts
- FLD-SERVICE_TYPE: verification_documentaire
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_titre
- FLD-DOUTES_DOCUMENTS: OUI

### missing_fields (ordered by priority)
1. FLD-CITY — Ville du terrain
2. FLD-NEIGHBORHOOD — Quartier
3. FLD-NUM_TITRE — Numéro de titre si connu
4. FLD-DOCUMENTS_DISPONIBLES — Documents en possession
5. FLD-DELAI_SOUHAITE — Délai de vérification

### next_question
"Une vérification documentaire pour un terrain. Dans quelle ville se trouve le terrain et avez-vous déjà des documents ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander les détails du terrain
- Proposer un expert juridique
- Rassurer sur le processus

### forbidden_actions
- Donner un avis juridique sans expertise
- Minimiser les doutes de l'acheteur

### matching_criteria
- FLD-SERVICE_TYPE: hard_constraint + weight 35

---

## SCENARIO-071: Demande conseil juridique

### context
- **request_family**: REAL_ESTATE_SERVICE
- **property_type**: SERVICE
- **transaction_type**: SERVICE
- **requester_profile**: héritier

### initial_message
"Bonjour, j'ai besoin de conseils juridiques pour une succession immobilière à Douala."

### extracted_facts
- FLD-SERVICE_TYPE: conseil_juridique
- FLD-CITY: Douala
- FLD-CONTEXTE: succession
- FLD-TYPE_BIEN: immobilier

### missing_fields (ordered by priority)
1. FLD-NATURE_BIEN — Nature du bien successoral
2. FLD-NOMBRE_AYANTS_DROIT — Nombre d'héritiers
3. FLD-DOCUMENTS_EXISTANTS — Acte de décès, titre, etc.
4. FLD-DELAI — Délai de traitement
5. FLD-URGENCE — Degré d'urgence

### next_question
"Un conseil juridique pour une succession immobilière à Douala. Pouvez-vous me donner plus de détails sur le bien concerné ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander les détails de la succession
- Proposer un avocat spécialisé
- Discuter des documents nécessaires

### forbidden_actions
- Donner des conseils juridiques spécifiques sans expertise
- Ignorer les spécificités successorales

### matching_criteria
- FLD-SERVICE_TYPE: hard_constraint + weight 30
- FLD-CONTEXTE: hard_constraint + weight 25

---

## SCENARIO-072: Demande déménagement

### context
- **request_family**: REAL_ESTATE_SERVICE
- **property_type**: SERVICE
- **transaction_type**: SERVICE
- **requester_profile**: particulier

### initial_message
"Salut, je déménage de Yaoundé à Douala, je cherche un service de déménagement fiable."

### extracted_facts
- FLD-SERVICE_TYPE: demenagement
- FLD-CITY_DEPART: Yaoundé
- FLD-CITY_ARRIVEE: Douala
- FLD-TRANSACTION: SERVICE

### missing_fields (ordered by priority)
1. FLD-DATE_DEMENAGEMENT — Date du déménagement
2. FLD-VOLUME — Volume à déménager
3. FLD-NOMBRE_PIECES — Nombre de pièces
4. FLD-BUDGET — Budget déménagement
5. FLD-SERVICES_COMPLEMENTAIRES — Emballage, montage meubles ?

### next_question
"Un déménagement de Yaoundé à Douala. Pour quelle date et quel est le volume approximatif à déménager ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander date et volume
- Proposer des déménageurs partenaires
- Discuter des services inclus

### forbidden_actions
- Proposer des devis sans volume
- Ignorer les spécificités inter-villes

### matching_criteria
- FLD-SERVICE_TYPE: hard_constraint + weight 30
- FLD-CITY_DEPART: hard_constraint + weight 15
- FLD-CITY_ARRIVEE: hard_constraint + weight 15

---

## SCENARIO-073: Demande de visite de propriété

### context
- **request_family**: REAL_ESTATE_SERVICE
- **property_type**: SERVICE
- **transaction_type**: RENT
- **requester_profile**: locataire potentiel

### initial_message
"Bonjour, j'ai vu une annonce pour un studio à Douala, je veux visiter."

### extracted_facts
- FLD-SERVICE_TYPE: visite_propriete
- FLD-CITY: Douala
- FLD-PROPERTY_TYPE: studio

### missing_fields (ordered by priority)
1. FLD-REFERENCE_ANNONCE — Référence de l'annonce
2. FLD-NEIGHBORHOOD — Quartier
3. FLD-DISPONIBILITE — Disponibilités visite
4. FLD-PROFIL_VISITEUR — Nom, contact

### next_question
"Une visite de studio à Douala ! Avez-vous une référence d'annonce ou le quartier où se trouve le studio ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander la référence
- Proposer des créneaux de visite
- Collecter les coordonnées

### forbidden_actions
- Organiser une visite sans référence
- Partager l'adresse sans confirmation

### matching_criteria
- FLD-SERVICE_TYPE: hard_constraint + weight 30
- FLD-CITY: hard_constraint + weight 20

---

## SCENARIO-074: Demande inspection technique

### context
- **request_family**: REAL_ESTATE_SERVICE
- **property_type**: SERVICE
- **transaction_type**: SERVICE
- **requester_profile**: acheteur

### initial_message
"Je veux faire inspecter une maison que je compte acheter à Buea, pour vérifier l'état général."

### extracted_facts
- FLD-SERVICE_TYPE: inspection_technique
- FLD-PROPERTY_TYPE: maison_individuelle
- FLD-CITY: Buea
- FLD-TRANSACTION: BUY

### missing_fields (ordered by priority)
1. FLD-SURFACE — Surface du bien
2. FLD-AGE — Âge du bâtiment
3. FLD-DISPONIBILITE — Disponibilité visite inspection
4. FLD-POINTS_ATTENTION — Points spécifiques à vérifier
5. FLD-BUDGET — Budget inspection

### next_question
"Une inspection technique pour une maison à Buea. Y a-t-il des points spécifiques que vous voulez vérifier (toiture, électricité, plomberie) ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander les points d'attention
- Proposer des inspecteurs partenaires
- Discuter des garanties

### forbidden_actions
- Ignorer l'âge du bâtiment
- Proposer une inspection sans visite

### matching_criteria
- FLD-SERVICE_TYPE: hard_constraint + weight 30
- FLD-CITY: hard_constraint + weight 20

---

## Scenarios 75-80: Listing — Mise en location

## SCENARIO-075: Propriétaire met studio en location

### context
- **request_family**: LISTING
- **property_type**: studio
- **transaction_type**: RENT
- **requester_profile**: propriétaire bailleur

### initial_message
"Bonjour, je veux mettre mon studio en location à Douala, 80 000 FCFA par mois."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: studio
- FLD-CITY: Douala
- FLD-LOYER: 80000
- FLD-INTENT: SELL_PROPERTY
- FLD-MEUBLE: NON

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-SURFACE — Surface du studio
3. FLD-ETAT — État du studio
4. FLD-DISPONIBILITE — Disponibilité
5. FLD-CUISINE — Type de cuisine
6. FLD-DOUCHES — Type de douche

### next_question
"Vous voulez mettre votre studio en location à Douala pour 80 000 FCFA. Dans quel quartier se trouve-t-il ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander le quartier
- Collecter les caractéristiques
- Préparer la fiche annonce

### forbidden_actions
- Publier l'annonce sans toutes les informations
- Fixer un rendez-vous sans voir le bien

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 20
- FLD-LOYER: hard_constraint + weight 20

---

## SCENARIO-076: Propriétaire met appartement en location

### context
- **request_family**: LISTING
- **property_type**: appartement_non_meuble
- **transaction_type**: RENT
- **requester_profile**: propriétaire bailleur

### initial_message
"Je veux louer mon appartement 2 pièces à Yaoundé, quartier Mvog-Mbi, 120 000 FCFA."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: appartement_non_meuble
- FLD-CITY: Yaoundé
- FLD-NEIGHBORHOOD: Mvog-Mbi
- FLD-LOYER: 120000
- FLD-PIECES: 2

### missing_fields (ordered by priority)
1. FLD-SURFACE — Surface habitable
2. FLD-ETAGE — Étage
3. FLD-DISPONIBILITE — Date de disponibilité
4. FLD-DOUCHES — Salle de bain
5. FLD-CUISINE — Cuisine
6. FLD-CHARGES — Charges incluses ?
7. FLD-PHOTOS — Photos du bien

### next_question
"Un appartement 2 pièces à Mvog-Mbi, Yaoundé pour 120 000 FCFA. Quelle est la surface et à quel étage se trouve-t-il ?"

### readiness_level
MINIMUM_SEARCH_READY

### allowed_actions
- Demander les caractéristiques
- Proposer de prendre des photos
- Préparer la publication

### forbidden_actions
- Publier sans photos
- Fixer le prix sans vérifier le marché

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-NEIGHBORHOOD: hard_constraint + weight 20
- FLD-LOYER: hard_constraint + weight 20

---

## SCENARIO-077: Propriétaire met villa en location

### context
- **request_family**: LISTING
- **property_type**: villa
- **transaction_type**: RENT
- **requester_profile**: propriétaire bailleur

### initial_message
"Bonjour, je cherche à louer ma villa 5 chambres à Douala Bonamoussadi, 350 000 FCFA."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: villa
- FLD-CITY: Douala
- FLD-NEIGHBORHOOD: Bonamoussadi
- FLD-CHAMBRES: 5
- FLD-LOYER: 350000

### missing_fields (ordered by priority)
1. FLD-SURFACE — Surface habitable
2. FLD-SALONS — Nombre de salons
3. FLD-DOUCHES — Nombre de salles de bain
4. FLD-PARKING — Parking
5. FLD-COUR — Cour/jardin
6. FLD-DISPONIBILITE — Date de disponibilité
7. FLD-PHOTOS — Photos

### next_question
"Une villa 5 chambres à Bonamoussadi pour 350 000 FCFA. Combien de salons et de salles de bain ? A-t-elle un jardin ?"

### readiness_level
MINIMUM_SEARCH_READY

### allowed_actions
- Demander les caractéristiques détaillées
- Proposer une visite pour photos
- Estimer le prix du marché

### forbidden_actions
- Publier sans caractéristiques complètes
- Sous-estimer le nombre de pièces

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-NEIGHBORHOOD: hard_constraint + weight 20
- FLD-LOYER: hard_constraint + weight 15

---

## SCENARIO-078: Agence mandat de location

### context
- **request_family**: LISTING
- **property_type**: appartement_non_meuble
- **transaction_type**: RENT
- **requester_profile**: agence immobilière

### initial_message
"Bonjour, nous sommes une agence immobilière à Douala et nous voulons confier 5 appartements à LAWIM pour location."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: appartement_non_meuble
- FLD-CITY: Douala
- FLD-PROFIL: agence_immobiliere
- FLD-NOMBRE_BIENS: 5

### missing_fields (ordered by priority)
1. FLD-MANDAT_TYPE — Type de mandat
2. FLD-LOYER_MOYEN — Loyer moyen par bien
3. FLD-QUARTIERS — Quartiers des biens
4. FLD-DISPONIBILITE — Disponibilités
5. FLD-DOCUMENTS_AGENCE — Registre de commerce, agrément

### next_question
"5 appartements à Douala en mandat de location. Pouvez-vous nous donner les quartiers et les loyers prévus ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander les détails du mandat
- Vérifier les documents de l'agence
- Proposer une convention de partenariat

### forbidden_actions
- Accepter sans vérifier l'agrément
- Publier sans mandat signé

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-NOMBRE_BIENS: hard_constraint + weight 20
- FLD-PROFIL: hard_constraint + weight 20

---

## SCENARIO-079: Mandataire avec procuration

### context
- **request_family**: LISTING
- **property_type**: villa
- **transaction_type**: RENT
- **requester_profile**: mandataire

### initial_message
"Bonjour, mon frère habite en France et il veut que je gère la location de sa villa à Yaoundé."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: villa
- FLD-CITY: Yaoundé
- FLD-PROPRIETAIRE: absent (diaspora)
- FLD-MANDATAIRE: frère
- FLD-PROCURATION: à vérifier

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier de la villa
2. FLD-LOYER — Loyer souhaité
3. FLD-CHAMBRES — Nombre de chambres
4. FLD-DISPONIBILITE — Disponibilité
5. FLD-PROCURATION — Document de procuration
6. FLD-SURFACE — Surface

### next_question
"La villa de votre frère à Yaoundé. Dans quel quartier se trouve-t-elle et quel loyer souhaite-t-il ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander les détails du bien
- Vérifier la procuration
- Contacter le propriétaire pour confirmation

### forbidden_actions
- Publier sans vérifier la procuration
- Payer le mandataire sans accord du propriétaire

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 20

---

## SCENARIO-080: Mise en location meublée

### context
- **request_family**: LISTING
- **property_type**: studio_meuble
- **transaction_type**: RENT
- **requester_profile**: propriétaire

### initial_message
"Salut, je veux mettre mon studio meublé en location courte durée à Douala, près de l'aéroport."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: studio_meuble
- FLD-CITY: Douala
- FLD-ZONE: près aéroport
- FLD-DUREE: courte_duree
- FLD-MEUBLE: OUI

### missing_fields (ordered by priority)
1. FLD-LOYER_NUIT — Prix par nuit ou par mois
2. FLD-NEIGHBORHOOD — Quartier précis
3. FLD-DISPONIBILITE — Calendrier de disponibilité
4. FLD-EQUIPEMENTS — Liste équipements
5. FLD-PHOTOS — Photos

### next_question
"Un studio meublé près de l'aéroport de Douala. Quel est le prix par nuit et dans quel quartier exactement ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander prix et localisation
- Collecter la liste des équipements
- Préparer l'annonce courte durée

### forbidden_actions
- Publier sans photos
- Confondre location courte et longue durée

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-PROPERTY_TYPE: hard_constraint + weight 20
- FLD-DUREE: hard_constraint + weight 20

---

## Scenarios 81-86: Listing — Mise en vente

## SCENARIO-081: Propriétaire vend terrain titré

### context
- **request_family**: LISTING
- **property_type**: terrain_titre
- **transaction_type**: SELL
- **requester_profile**: propriétaire

### initial_message
"Bonjour, je vends mon terrain titré à Yaoundé, 500 m², numéro TF au complet."

### extracted_facts
- FLD-TRANSACTION: SELL
- FLD-PROPERTY_TYPE: terrain_titre
- FLD-CITY: Yaoundé
- FLD-SURFACE: 500
- FLD-NUM_TITRE: OUI

### missing_fields (ordered by priority)
1. FLD-PRIX_VENTE — Prix de vente
2. FLD-NEIGHBORHOOD — Quartier
3. FLD-DOCUMENTS — Copies des documents
4. FLD-USAGE — Usage prévu (constructible ?)
5. FLD-PHOTOS — Photos du terrain

### next_question
"Un terrain titré de 500 m² à Yaoundé avec TF complet. Dans quel quartier et à quel prix souhaitez-vous vendre ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander prix et quartier
- Vérifier les documents
- Proposer une estimation

### forbidden_actions
- Publier sans vérifier le titre foncier
- Fixer un prix sans analyse du marché

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-PROPERTY_TYPE: hard_constraint + weight 20
- FLD-SURFACE: hard_constraint + weight 20

---

## SCENARIO-082: Propriétaire vend villa

### context
- **request_family**: LISTING
- **property_type**: villa
- **transaction_type**: SELL
- **requester_profile**: propriétaire

### initial_message
"Je vends ma villa à Douala Bonapriso, 4 chambres, 3 salles de bain, grand salon, prix 120 millions."

### extracted_facts
- FLD-TRANSACTION: SELL
- FLD-PROPERTY_TYPE: villa
- FLD-CITY: Douala
- FLD-NEIGHBORHOOD: Bonapriso
- FLD-CHAMBRES: 4
- FLD-DOUCHES: 3
- FLD-SALONS: 1
- FLD-PRIX: 120000000

### missing_fields (ordered by priority)
1. FLD-SURFACE — Surface habitable
2. FLD-ETAT — État de la villa
3. FLD-DISPONIBILITE — Disponibilité visite
4. FLD-DOCUMENTS — Titre de propriété
5. FLD-PHOTOS — Photos
6. FLD-PARKING — Parking
7. FLD-CUISINE — Type de cuisine

### next_question
"Une villa 4 chambres à Bonapriso pour 120 millions. Quelle est la surface habitable et quel est l'état général ?"

### readiness_level
MINIMUM_SEARCH_READY

### allowed_actions
- Demander surface et état
- Vérifier les documents
- Planifier une séance photo

### forbidden_actions
- Publier sans documents légaux
- Négliger les photos professionnelles

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-NEIGHBORHOOD: hard_constraint + weight 20
- FLD-PRIX: hard_constraint + weight 20

---

## SCENARIO-083: Vente appartement avec documents

### context
- **request_family**: LISTING
- **property_type**: appartement_non_meuble
- **transaction_type**: SELL
- **requester_profile**: propriétaire

### initial_message
"Je vends mon appartement à Yaoundé Bastos, 3 chambres, 85 m², avec tous les documents, 65 millions."

### extracted_facts
- FLD-TRANSACTION: SELL
- FLD-PROPERTY_TYPE: appartement_non_meuble
- FLD-CITY: Yaoundé
- FLD-NEIGHBORHOOD: Bastos
- FLD-CHAMBRES: 3
- FLD-SURFACE: 85
- FLD-PRIX: 65000000
- FLD-DOCUMENTS: OUI

### missing_fields (ordered by priority)
1. FLD-DOUCHES — Nombre de salles de bain
2. FLD-SALONS — Salon
3. FLD-ETAGE — Étage
4. FLD-DISPONIBILITE — Disponibilité visite
5. FLD-PHOTOS — Photos
6. FLD-ETAT — État

### next_question
"Un appartement 3 chambres à Bastos, 85 m², 65 millions avec documents. Combien de salles de bain et à quel étage ?"

### readiness_level
MINIMUM_SEARCH_READY

### allowed_actions
- Demander les caractéristiques
- Vérifier les documents
- Préparer l'annonce

### forbidden_actions
- Publier sans vérifier les documents
- Ignorer les détails des pièces

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-NEIGHBORHOOD: hard_constraint + weight 20
- FLD-PRIX: hard_constraint + weight 20
- FLD-SURFACE: hard_constraint + weight 15

---

## SCENARIO-084: Mandat de vente exclusif

### context
- **request_family**: LISTING
- **property_type**: villa
- **transaction_type**: SELL
- **requester_profile**: propriétaire

### initial_message
"Je veux confier la vente de ma villa à LAWIM en exclusivité. Elle est à Douala, 250 millions."

### extracted_facts
- FLD-TRANSACTION: SELL
- FLD-PROPERTY_TYPE: villa
- FLD-CITY: Douala
- FLD-PRIX: 250000000
- FLD-MANDAT_TYPE: EXCLUSIF

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier
2. FLD-CHAMBRES — Nombre de chambres
3. FLD-SURFACE — Surface
4. FLD-DISPONIBILITE — Disponibilité
5. FLD-DOCUMENTS — Titre de propriété
6. FLD-DUREE_MANDAT — Durée du mandat

### next_question
"Un mandat exclusif pour une villa à Douala à 250 millions. Dans quel quartier et combien de chambres ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander les détails du bien
- Proposer une convention de mandat exclusif
- Discuter de la stratégie de vente

### forbidden_actions
- Accepter un mandat sans voir le bien
- Négliger les termes du mandat

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-PRIX: hard_constraint + weight 20
- FLD-MANDAT_TYPE: hard_constraint + weight 20

---

## SCENARIO-085: Vente immeuble de rapport

### context
- **request_family**: LISTING
- **property_type**: immeuble_rapport
- **transaction_type**: SELL
- **requester_profile**: propriétaire

### initial_message
"Bonjour, je vends mon immeuble de rapport à Douala, 8 studios, 400 millions."

### extracted_facts
- FLD-TRANSACTION: SELL
- FLD-PROPERTY_TYPE: immeuble_rapport
- FLD-CITY: Douala
- FLD-NOMBRE_LOGEMENTS: 8
- FLD-PRIX: 400000000

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier
2. FLD-SURFACE_TERRAIN — Surface terrain
3. FLD-SURFACE_BATIE — Surface bâtie
4. FLD-ETAT — État de l'immeuble
5. FLD-RENDEMENT — Rendement locatif actuel
6. FLD-DISPONIBILITE — Disponibilité
7. FLD-DOCUMENTS — Titre foncier

### next_question
"Un immeuble de rapport de 8 studios à Douala pour 400 millions. Dans quel quartier et quel est le rendement actuel ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander quartier et rendement
- Vérifier les documents
- Proposer une étude de rentabilité

### forbidden_actions
- Publier sans indication de rendement
- Ignorer les aspects légaux

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-PRIX: hard_constraint + weight 20
- FLD-NOMBRE_LOGEMENTS: hard_constraint + weight 20

---

## SCENARIO-086: Vente terrain non titré

### context
- **request_family**: LISTING
- **property_type**: terrain_non_titre
- **transaction_type**: SELL
- **requester_profile**: propriétaire

### initial_message
"Je veux vendre un terrain à Mbankomo, 600 m², avec certificat de propriété, 5 millions."

### extracted_facts
- FLD-TRANSACTION: SELL
- FLD-PROPERTY_TYPE: terrain_non_titre
- FLD-CITY: Mbankomo
- FLD-SURFACE: 600
- FLD-PRIX: 5000000
- FLD-DOCUMENT: CERTIFICAT_PROPRIETE

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier ou village
2. FLD-USAGE — Usage (constructible ?)
3. FLD-ACCESSIBILITE — Accès
4. FLD-DISPONIBILITE — Disponibilité
5. FLD-PHOTOS — Photos
6. FLD-COORDONNEES_GPS — Coordonnées GPS

### next_question
"Un terrain de 600 m² avec certificat à Mbankomo pour 5 millions. Dans quel secteur exactement et la route est-elle accessible ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander localisation précise
- Vérifier le certificat
- Discuter de l'accessibilité

### forbidden_actions
- Publier sans vérifier le document
- Garantir la constructibilité sans vérification

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-SURFACE: hard_constraint + weight 20
- FLD-PRIX: hard_constraint + weight 20
- FLD-DOCUMENT: hard_constraint + weight 15

---

## Scenarios 87-100+: Special cases

## SCENARIO-087: Investisseur diaspora recherche terrain

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_titre
- **transaction_type**: BUY
- **requester_profile**: diaspora

### initial_message
"I'm based in the US and want to buy land in Cameroon for investment. Looking for titled land in Douala or Yaoundé."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_titre
- FLD-DIASPORA: OUI
- FLD-PAYS_RESIDENCE: US
- FLD-USAGE: INVESTISSEMENT
- FLD-CITY_ALTERNATIVES: Douala, Yaoundé

### missing_fields (ordered by priority)
1. FLD-CITY — Ville précise à choisir
2. FLD-BUDGET_MAX — Budget non mentionné
3. FLD-SURFACE — Surface recherchée
4. FLD-BESOIN_ACCOMPAGNEMENT — Accompagnement sur place

### next_question
"Great! A titled land for investment in Douala or Yaoundé. Which city do you prefer and what's your budget?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Confirmer diaspora
- Demander ville et budget
- Proposer accompagnement spécifique diaspora

### forbidden_actions
- Proposer sans accompagnement sur place
- Ignorer le décalage horaire

### matching_criteria
- FLD-DIASPORA: ranking_preference + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 25

---

## SCENARIO-088: Investisseur rendement locatif

### context
- **request_family**: COMMERCIAL_SEARCH
- **property_type**: immeuble_rapport
- **transaction_type**: BUY
- **requester_profile**: investisseur

### initial_message
"Je cherche un immeuble avec un bon rendement locatif à Douala, budget 200 millions max."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: immeuble_rapport
- FLD-CITY: Douala
- FLD-BUDGET_MAX: 200000000
- FLD-BUDGET_TYPE: TOTAL_PRICE

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-RENDEMENT_ATTENDU — Rendement attendu
3. FLD-NOMBRE_LOGEMENTS — Nombre minimum de logements
4. FLD-FINANCING — Financement
5. FLD-DISPONIBILITE — Délai d'achat

### next_question
"Un immeuble de rapport à Douala pour 200 millions. Quel rendement attendez-vous et dans quel quartier ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander quartier et rendement
- Discuter des critères de rentabilité
- Proposer une analyse de marché

### forbidden_actions
- Proposer des biens sans calcul de rendement
- Ignorer les charges et taxes

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-RENDEMENT_ATTENDU: soft_constraint + weight 20

---

## SCENARIO-089: Changement de type de bien en cours

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: studio (initial)
- **transaction_type**: RENT
- **requester_profile**: tenant

### initial_message
"Je cherche un studio à Douala, 100 000 FCFA."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: studio
- FLD-CITY: Douala
- FLD-BUDGET_MAX: 100000
- FLD-BUDGET_TYPE: MONTHLY_RENT

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné

### next_question
(the user changes mind)
"Finalement je pense qu'un studio est trop petit. Je cherche plutôt un appartement 1 chambre."

### field_updates
- FLD-PROPERTY_TYPE: appartement_non_meuble (changed from studio)
- FLD-CHAMBRES: 1

### revalidation
- Same budget may be tight for 1-bedroom in Douala
- Quartier still needed

### next_question_after_change
"Pas de problème ! Un appartement 1 chambre à Douala pour 100 000 FCFA. Le budget est un peu serré pour un 1 chambre, mais on peut chercher. Dans quel quartier ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Accepter le changement de type
- Revalider le budget pour le nouveau type
- Demander le quartier

### forbidden_actions
- Ignorer le changement de préférence
- Continuer avec l'ancien type de bien

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 20 (updated)

---

## SCENARIO-090: Changement de budget

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: appartement_non_meuble
- **transaction_type**: RENT
- **requester_profile**: famille

### initial_message
"Je cherche un appartement 2 chambres à Douala, max 200 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: appartement_non_meuble
- FLD-CITY: Douala
- FLD-BUDGET_MAX: 200000
- FLD-CHAMBRES: 2

### next_question
"Dans quel quartier cherchez-vous ?"
(user) "Bonamoussadi. Ah et finalement je peux mettre jusqu'à 300 000."

### field_updates
- FLD-NEIGHBORHOOD: Bonamoussadi
- FLD-BUDGET_MAX: 300000 (updated)

### revalidation
- Budget increase → broader options
- Quartier now known → MINIMUM_SEARCH_READY

### next_question_after_change
"Bonamoussadi, parfait ! Avec 300 000 FCFA nous avons plus d'options. Je lance la recherche tout de suite."

### readiness_level
MINIMUM_SEARCH_READY

### allowed_actions
- Lancer la recherche
- Présenter les résultats
- Proposer des critères de raffinement

### forbidden_actions
- Continuer à poser des questions avant la recherche
- Utiliser l'ancien budget

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-NEIGHBORHOOD: hard_constraint + weight 20
- FLD-BUDGET_MAX: hard_constraint + weight 20 (updated)

---

## SCENARIO-091: Changement de ville

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: studio
- **transaction_type**: RENT
- **requester_profile**: jeune professionnel

### initial_message
"Je cherche un studio à Yaoundé."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: studio
- FLD-CITY: Yaoundé

### next_question
"Quel budget ?"
(user) "150 000. Ah non finalement je suis muté à Douala."

### field_updates
- FLD-CITY: Douala (changed from Yaoundé)
- FLD-BUDGET_MAX: 150000

### revalidation
- City changed → reset neighborhood
- Budget remains valid for Douala studios

### next_question_after_change
"Pas de souci, Douala c'est très bien aussi ! Un studio à Douala pour 150 000. Dans quel quartier ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Accepter le changement de ville
- Demander le quartier à Douala
- Réinitialiser les critères liés à la ville

### forbidden_actions
- Continuer avec les données de Yaoundé
- Ignorer l'impact sur les résultats

### matching_criteria
- FLD-CITY: hard_constraint + weight 30 (updated)
- FLD-BUDGET_MAX: hard_constraint + weight 25

---

## SCENARIO-092: Utilisateur imprécis corrigé

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: UNDETERMINED
- **transaction_type**: RENT
- **requester_profile**: particulier

### initial_message
"Bonjour, je cherche une maison."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: UNDETERMINED
- FLD-INTENT_CONFIDENCE: 0.3

### missing_fields (ordered by priority)
1. FLD-PROPERTY_TYPE — Type de bien trop vague
2. FLD-CITY — Ville non mentionnée
3. FLD-BUDGET_MAX — Budget non mentionné

### next_question
"Bonjour ! Vous cherchez une maison à louer. Pouvez-vous être plus précis ? C'est une villa, une maison individuelle, un duplex ou autre chose ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Clarifier le type de bien
- Proposer des choix
- Demander la ville

### forbidden_actions
- Lancer une recherche avec un type vague
- Supposer le type de bien

### matching_criteria
- FLD-TRANSACTION: hard_constraint + weight 25

---

## SCENARIO-093: Urgence élevée

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: chambre_moderne
- **transaction_type**: RENT
- **requester_profile**: urgent

### initial_message
"Bonjour c'est urgent ! Je dois quitter mon logement dans 3 jours, je cherche une chambre moderne à Douala."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: chambre_moderne
- FLD-CITY: Douala
- FLD-URGENCE: HAUTE
- FLD-DELAI: 3 jours

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-NEIGHBORHOOD — Quartier non mentionné
3. FLD-DOUCHES — Type de douche

### next_question
"Je comprends l'urgence, on va faire vite ! Quel budget maximum et dans quel quartier ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Accélérer le processus
- Prioriser la recherche
- Proposer des visites rapides
- Réduire les questions non essentielles

### forbidden_actions
- Poser des questions non prioritaires
- Ralentir le processus
- Ignorer l'urgence

### matching_criteria
- FLD-CITY: hard_constraint + weight 30
- FLD-PROPERTY_TYPE: hard_constraint + weight 20
- FLD-URGENCE: ranking_preference + weight 15

---

## SCENARIO-094: Demande escale humaine

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: UNDETERMINED
- **transaction_type**: UNDETERMINED
- **requester_profile**: personne âgée

### initial_message
"Bonjour, je ne comprends pas trop comment ça marche. J'ai entendu parler de LAWIM. Vous pouvez m'aider ? Je veux acheter quelque chose."

### extracted_facts
- FLD-INTENT_CONFIDENCE: 0.2
- FLD-TRANSACTION: BUY (probable)

### missing_fields (ordered by priority)
1. FLD-TRANSACTION — À confirmer
2. FLD-PROPERTY_TYPE — Type de bien
3. FLD-CITY — Ville
4. FLD-BUDGET_MAX — Budget

### next_question
"Bonjour et bienvenue chez LAWIM ! Je suis là pour vous aider. Vous voulez acheter. C'est pour acheter une maison, un terrain ou autre chose ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Accueillir chaleureusement
- Guider pas à pas
- Proposer une assistance téléphonique si nécessaire
- Utiliser un langage simple

### forbidden_actions
- Aller trop vite
- Utiliser du jargon technique
- Ignorer les signes de confusion

### matching_criteria
- N/A (human escalation if confusion persists)

---

## SCENARIO-095: Budget irréaliste pour la zone

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: villa
- **transaction_type**: RENT
- **requester_profile**: particulier

### initial_message
"Je cherche une villa 4 chambres à Bastos Yaoundé, budget 150 000."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: villa
- FLD-CITY: Yaoundé
- FLD-NEIGHBORHOOD: Bastos
- FLD-BUDGET_MAX: 150000
- FLD-CHAMBRES: 4

### validation_issues
- FLD-BUDGET_MAX: Trop bas pour une villa 4 chambres à Bastos (minimum 500k-800k)

### next_question
"Une villa 4 chambres à Bastos pour 150 000 FCFA. Je dois vous informer que les villas à Bastos sont généralement entre 500 000 et 1 000 000 FCFA. Votre budget est peut-être trop juste pour ce quartier. Souhaitez-vous : (1) Augmenter le budget, (2) Chercher un autre quartier, ou (3) Chercher un studio ou appartement à Bastos ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Informer de la réalité du marché
- Proposer des alternatives
- Ajuster les attentes

### forbidden_actions
- Proposer des biens inexistants
- Ignorer l'inadéquation budget/quartier

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-NEIGHBORHOOD: hard_constraint + weight 20
- FLD-BUDGET_MAX: hard_constraint + weight 25 (blocking)

---

## SCENARIO-096: Propriétaire multiple signataires

### context
- **request_family**: LISTING
- **property_type**: villa
- **transaction_type**: SELL
- **requester_profile**: famille (co-indivisaires)

### initial_message
"Bonjour, nous sommes 4 frères et soeurs et nous voulons vendre la villa familiale à Yaoundé."

### extracted_facts
- FLD-TRANSACTION: SELL
- FLD-PROPERTY_TYPE: villa
- FLD-CITY: Yaoundé
- FLD-NOMBRE_SIGNATAIRES: 4
- FLD-INDIVISION: OUI

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier
2. FLD-PRIX_VENTE — Prix de vente
3. FLD-SURFACE — Surface
4. FLD-CHAMBRES — Nombre de chambres
5. FLD-IDENTITE_SIGNATAIRES — Identité de tous les propriétaires
6. FLD-DOCUMENTS — Titre de propriété, acte de succession
7. FLD-MANDAT_REPRESENTANT — Mandataire désigné

### next_question
"La vente de la villa familiale à Yaoundé avec 4 co-indivisaires. Dans quel quartier se trouve-t-elle et quel prix souhaitez-vous ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander les détails du bien
- Vérifier l'acte de succession
- Proposer un notaire pour gérer l'indivision

### forbidden_actions
- Accepter un seul signataire sans procuration
- Ignorer les aspects légaux de l'indivision

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-NOMBRE_SIGNATAIRES: hard_constraint + weight 20

---

## SCENARIO-097: Succession et indivision

### context
- **request_family**: REAL_ESTATE_SERVICE
- **property_type**: SERVICE
- **transaction_type**: SERVICE
- **requester_profile**: héritier

### initial_message
"Bonjour, mon père est décédé et a laissé un terrain à Douala. Nous sommes 5 enfants. On veut vendre mais on ne sait pas comment faire."

### extracted_facts
- FLD-SERVICE_TYPE: conseil_juridique
- FLD-CONTEXTE: succession
- FLD-CITY: Douala
- FLD-NOMBRE_AYANTS_DROIT: 5
- FLD-TRANSACTION: SELL (indirect)

### missing_fields (ordered by priority)
1. FLD-PROPERTY_TYPE — Type de bien
2. FLD-DOCUMENTS_EXISTANTS — Acte de décès, titre
3. FLD-NEIGHBORHOOD — Quartier
4. FLD-BESOIN_NOTAIRE — Notaire déjà saisi ?
5. FLD-URGENCE — Degré d'urgence

### next_question
"Je vous présente mes condoléances. Nous allons vous guider. De quel type de bien s'agit-il et avez-vous déjà les documents (acte de décès, titre foncier) ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Proposer un accompagnement complet
- Mettre en relation avec un notaire
- Expliquer les étapes de la succession

### forbidden_actions
- Donner des conseils juridiques non vérifiés
- Proposer une vente sans règlement de la succession

### matching_criteria
- FLD-SERVICE_TYPE: hard_constraint + weight 25
- FLD-CONTEXTE: hard_constraint + weight 25

---

## SCENARIO-098: Terrain avec servitude

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_titre
- **transaction_type**: BUY
- **requester_profile**: particulier averti

### initial_message
"Je cherche un terrain à Douala mais je veux être sûr qu'il n'y a pas de servitude qui bloque la construction."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_titre
- FLD-CITY: Douala
- FLD-SERVITUDE: à vérifier

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE — Surface recherchée
3. FLD-NEIGHBORHOOD — Quartier non mentionné
4. FLD-DOCUMENTS — Demander le RBUDGET_MAX et le cahier des charges

### next_question
"Un terrain titré sans servitude à Douala. Quel budget et dans quel quartier ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander budget et quartier
- Expliquer l'importance des vérifications
- Proposer un géomètre

### forbidden_actions
- Garantir l'absence de servitude sans vérification
- Minimiser les vérifications

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 25

---

## SCENARIO-099: Local commercial usage réglementé

### context
- **request_family**: COMMERCIAL_SEARCH
- **property_type**: local_commercial
- **transaction_type**: RENT
- **requester_profile**: restaurateur

### initial_message
"Je cherche un local pour ouvrir un bar-restaurant à Yaoundé, avec licence et tout en règle."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: local_commercial
- FLD-CITY: Yaoundé
- FLD-ACTIVITE: BAR_RESTAURANT
- FLD-LICENCE: OUI

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE_MIN — Surface minimum
3. FLD-NEIGHBORHOOD — Quartier
4. FLD-ZONAGE — Zone commerciale autorisée pour bar
5. FLD-NORME_SECURITE — Normes incendie et sécurité
6. FLD-HORAIRES_EXPLOITATION — Horaires d'ouverture

### next_question
"Un local pour bar-restaurant en règle à Yaoundé. Quel budget et dans quel quartier ? Notez que certains quartiers ont des restrictions pour les bars."

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander quartier et budget
- Vérifier les restrictions de zonage
- Proposer une vérification réglementaire

### forbidden_actions
- Proposer des locaux sans vérifier le zonage
- Ignorer les exigences de licence

### matching_criteria
- FLD-CITY: hard_constraint + weight 20
- FLD-ACTIVITE: hard_constraint + weight 25

---

## SCENARIO-100: Demande d'investissement promotion

### context
- **request_family**: FINANCING_REQUEST
- **property_type**: FINANCING
- **transaction_type**: FINANCE
- **requester_profile**: promoteur immobilier

### initial_message
"Je suis promoteur immobilier, je cherche un financement de 500 millions pour un projet de 12 appartements à Douala."

### extracted_facts
- FLD-OBJET_FINANCEMENT: financement_promotion
- FLD-MONTANT_RECHERCHE: 500000000
- FLD-NOMBRE_LOGEMENTS: 12
- FLD-CITY: Douala
- FLD-PROFIL_DEMANDEUR: promoteur

### missing_fields (ordered by priority)
1. FLD-APPORT — Apport du promoteur
2. FLD-COUT_TOTAL_PROJET — Coût total du projet
3. FLD-TERRAIN_DISPONIBLE — Terrain déjà acquis ?
4. FLD-PERMIS_CONSTRUIRE — Permis obtenu ?
5. FLD-DOCUMENTS_PROJET — Business plan, étude de marché
6. FLD-GARANTIES — Garanties offertes

### next_question
"Un financement de 500 millions pour 12 appartements à Douala. Quel est votre apport et avez-vous déjà le terrain et le permis ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander apport et documents
- Évaluer la viabilité du projet
- Proposer des investisseurs ou banques partenaires

### forbidden_actions
- Promettre un financement sans étude
- Ignorer les documents réglementaires

### matching_criteria
- FLD-OBJET_FINANCEMENT: hard_constraint + weight 30
- FLD-CITY: hard_constraint + weight 20

---

## SCENARIO-101: Construction sur terrain disponible

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: villa
- **transaction_type**: BUY
- **requester_profile**: particulier

### initial_message
"J'ai déjà un terrain à Douala et je cherche un constructeur pour bâtir ma villa 3 chambres."

### extracted_facts
- FLD-TERRAIN_DISPONIBLE: OUI
- FLD-CITY: Douala
- FLD-PROPERTY_TYPE: villa
- FLD-TRANSACTION: BUY (construction)
- FLD-CHAMBRES: 3

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier du terrain
2. FLD-BUDGET_CONSTRUCTION — Budget construction
3. FLD-DELAI — Délai souhaité
4. FLD-DOCUMENTS_TERRAIN — Titre foncier du terrain
5. FLD-SURFACE_TERRAIN — Surface terrain
6. FLD-PLANS — Plans disponibles ?

### next_question
"Vous avez un terrain à Douala et voulez construire une villa 3 chambres. Dans quel quartier et quel est votre budget de construction ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander budget et quartier
- Proposer des architectes et constructeurs
- Vérifier les documents du terrain

### forbidden_actions
- Proposer des terrains à acheter (terrain déjà disponible)
- Ignorer les documents du terrain

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-TERRAIN_DISPONIBLE: hard_constraint + weight 20

---

## SCENARIO-102: Rénovation partielle cuisine

### context
- **request_family**: PROFESSIONAL_SEARCH
- **property_type**: PROFESSIONAL
- **transaction_type**: FIND
- **requester_profile**: particulier

### initial_message
"Je cherche un cuisiniste ou un menuisier pour rénover ma cuisine à Yaoundé."

### extracted_facts
- FLD-TYPE_PRESTATION: recherche_professionnel
- FLD-PROFESSION_TYPE: cuisiniste_menuisier
- FLD-CITY: Yaoundé
- FLD-DESCRIPTION_BESOIN: rénovation cuisine

### missing_fields (ordered by priority)
1. FLD-SURFACE_CUISINE — Surface de la cuisine
2. FLD-BUDGET_TRAVAUX — Budget rénovation
3. FLD-DELAI — Délai souhaité
4. FLD-URGENCE — Degré d'urgence
5. FLD-MATERIAUX — Matériaux souhaités
6. FLD-TYPE_TRAVAUX — Type : meubles, plans de travail, électroménager

### next_question
"Un cuisiniste pour rénover votre cuisine à Yaoundé. Quelle est la surface de la cuisine et quel budget ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander surface et budget
- Proposer des cuisinistes partenaires
- Discuter des matériaux

### forbidden_actions
- Proposer des professionnels non spécialisés cuisine
- Ignorer le périmètre des travaux

### matching_criteria
- FLD-PROFESSION_TYPE: hard_constraint + weight 30
- FLD-CITY: hard_constraint + weight 20

---

## SCENARIO-103: Copropriété gestion syndic

### context
- **request_family**: REAL_ESTATE_SERVICE
- **property_type**: SERVICE
- **transaction_type**: SERVICE
- **requester_profile**: syndic de copropriété

### initial_message
"Bonjour, je suis le syndic d'une résidence de 20 appartements à Douala, nous cherchons un service de gestion professionnel."

### extracted_facts
- FLD-SERVICE_TYPE: gestion_copropriete
- FLD-CITY: Douala
- FLD-NOMBRE_LOGEMENTS: 20
- FLD-PROFIL_DEMANDEUR: syndic

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier
2. FLD-CHARGES_MENSUELLES — Budget charges copropriété
3. FLD-BESOINS_SPECIFIQUES — Travaux, sécurité, entretien
4. FLD-DOCUMENTS — Règlement de copropriété, PV d'AG

### next_question
"La gestion d'une copropriété de 20 appartements à Douala. Dans quel quartier et quels sont les besoins spécifiques ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander les détails de la résidence
- Proposer des services de gestion adaptés
- Discuter des charges et du budget

### forbidden_actions
- Proposer des services sans connaître les besoins
- Ignorer le règlement de copropriété

### matching_criteria
- FLD-SERVICE_TYPE: hard_constraint + weight 25
- FLD-CITY: hard_constraint + weight 20
- FLD-NOMBRE_LOGEMENTS: soft_constraint + weight 20

---

## SCENARIO-104: Recherche maison avec piscine

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: maison_individuelle
- **transaction_type**: RENT
- **requester_profile**: famille aisée

### initial_message
"Je cherche une maison individuelle avec piscine à Kribi pour les vacances, 1 semaine en décembre."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: maison_individuelle
- FLD-CITY: Kribi
- FLD-PISCINE: OUI
- FLD-DUREE: 1 semaine
- FLD-DISPONIBILITE: décembre
- FLD-USAGE: VACANCES

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-NEIGHBORHOOD — Secteur à Kribi
3. FLD-CHAMBRES — Nombre de chambres
4. FLD-PROXIMITE_PLAGE — Proximité plage

### next_question
"Une maison avec piscine à Kribi pour une semaine en décembre. Quel budget et quel secteur ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander budget et secteur
- Proposer des maisons de vacances
- Vérifier disponibilité en décembre

### forbidden_actions
- Proposer des locations longue durée
- Ignorer la saison haute (décembre)

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-PISCINE: hard_constraint + weight 25
- FLD-DUREE: hard_constraint + weight 20

---

## SCENARIO-105: Demande estimation terrain agricole

### context
- **request_family**: REAL_ESTATE_SERVICE
- **property_type**: SERVICE
- **transaction_type**: SERVICE
- **requester_profile**: agriculteur

### initial_message
"Bonjour, je voudrais faire estimer mon terrain agricole de 5 hectares à Mbandjock."

### extracted_facts
- FLD-SERVICE_TYPE: estimation_immobiliere
- FLD-PROPERTY_TYPE: terrain_agricole
- FLD-CITY: Mbandjock
- FLD-SURFACE: 50000

### missing_fields (ordered by priority)
1. FLD-DOCUMENT — Type de document
2. FLD-CULTURES — Cultures existantes
3. FLD-ACCESSIBILITE — Accès
4. FLD-EAU — Disponibilité en eau
5. FLD-TRANSACTION — Vente ou location ?

### next_question
"Une estimation pour 5 hectares de terrain agricole à Mbandjock. C'est pour une vente ou une location et quel type de document avez-vous ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander le but de l'estimation
- Évaluer les caractéristiques agricoles
- Proposer une visite

### forbidden_actions
- Estimer sans visite
- Ignorer la qualité des sols

### matching_criteria
- FLD-SERVICE_TYPE: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 25

---

## SCENARIO-106: Achat terrain avec construction existante

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_titre
- **transaction_type**: BUY
- **requester_profile**: investisseur

### initial_message
"Je cherche un terrain avec une petite construction existante à Limbé, pour rénover en guesthouse."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_titre
- FLD-CITY: Limbé
- FLD-CONSTRUCTION_EXISTANTE: OUI
- FLD-USAGE: INVESTISSEMENT_GUESTHOUSE

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE — Surface terrain
3. FLD-NEIGHBORHOOD — Quartier
4. FLD-ETAT_CONSTRUCTION — État du bâtiment existant
5. FLD-SURFACE_CONSTRUCTION — Surface bâtie

### next_question
"Un terrain avec construction existante à Limbé pour guesthouse. Quel budget et dans quel secteur ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander budget et secteur
- Discuter du potentiel touristique
- Évaluer les travaux de rénovation

### forbidden_actions
- Proposer des terrains nus
- Ignorer l'état de la construction

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-PROPERTY_TYPE: hard_constraint + weight 20
- FLD-USAGE: hard_constraint + weight 20

---

## SCENARIO-107: Logement de fonction entreprise

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: appartement_non_meuble
- **transaction_type**: RENT
- **requester_profile**: entreprise

### initial_message
"Nous sommes une entreprise à Douala et nous cherchons 3 appartements 2 chambres pour nos cadres."

### extracted_facts
- FLD-TRANSACTION: RENT
- FLD-PROPERTY_TYPE: appartement_non_meuble
- FLD-CITY: Douala
- FLD-CHAMBRES: 2
- FLD-NOMBRE_LOGEMENTS: 3
- FLD-PROFIL_DEMANDEUR: entreprise

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget par logement
2. FLD-NEIGHBORHOOD — Quartier souhaité
3. FLD-DUREE_BAIL — Durée du bail (souhaité)
4. FLD-DISPONIBILITE — Date d'entrée
5. FLD-MEUBLE — Meublé ou non ?

### next_question
"3 appartements 2 chambres pour cadres à Douala. Quel budget par logement et dans quel quartier ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander budget et quartier
- Proposer des solutions groupées
- Discuter de la durée du bail

### forbidden_actions
- Proposer un seul logement
- Ignorer le besoin de 3 logements proches

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-NOMBRE_LOGEMENTS: hard_constraint + weight 25

---

## SCENARIO-108: Demande agent nettoyage propriété

### context
- **request_family**: PROFESSIONAL_SEARCH
- **property_type**: PROFESSIONAL
- **transaction_type**: FIND
- **requester_profile**: propriétaire

### initial_message
"Bonjour, je cherche quelqu'un pour nettoyer ma villa à Douala avant mise en location."

### extracted_facts
- FLD-TYPE_PRESTATION: recherche_professionnel
- FLD-PROFESSION_TYPE: nettoyage_propriete
- FLD-CITY: Douala
- FLD-DESCRIPTION_BESOIN: nettoyage avant location
- FLD-TRANSACTION: RENT

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier
2. FLD-SURFACE — Surface à nettoyer
3. FLD-DISPONIBILITE — Date souhaitée
4. FLD-BUDGET — Budget
5. FLD-SERVICES — Nettoyage simple ou complet

### next_question
"Un service de nettoyage pour votre villa à Douala avant location. Dans quel quartier et pour quel jour ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander quartier et date
- Proposer des prestataires de nettoyage
- Discuter du périmètre des travaux

### forbidden_actions
- Proposer des professionnels non vérifiés
- Ignorer la surface exacte

### matching_criteria
- FLD-PROFESSION_TYPE: hard_constraint + weight 30
- FLD-CITY: hard_constraint + weight 20

---

## SCENARIO-109: Achat studio pour investissement

### context
- **request_family**: RESIDENTIAL_SEARCH
- **property_type**: studio
- **transaction_type**: BUY
- **requester_profile**: investisseur

### initial_message
"Je cherche un studio à acheter à Douala pour le louer ensuite, budget 15 millions."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: studio
- FLD-CITY: Douala
- FLD-BUDGET_MAX: 15000000
- FLD-BUDGET_TYPE: TOTAL_PRICE
- FLD-USAGE: INVESTISSEMENT

### missing_fields (ordered by priority)
1. FLD-NEIGHBORHOOD — Quartier non mentionné
2. FLD-ETAT — État du studio
3. FLD-DISPONIBILITE — Délai d'achat
4. FLD-RENDEMENT_ATTENDU — Rendement locatif attendu
5. FLD-FINANCING — Comptant ou crédit

### next_question
"Un studio à acheter pour investissement locatif à Douala, 15 millions. Dans quel quartier ?"

### readiness_level
MINIMUM_INTAKE_READY

### allowed_actions
- Demander le quartier
- Discuter du potentiel locatif
- Évaluer le rendement

### forbidden_actions
- Proposer des studios non rentables
- Ignorer l'aspect investissement

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-BUDGET_MAX: hard_constraint + weight 20
- FLD-USAGE: hard_constraint + weight 20

---

## SCENARIO-110: Terrain avec viabilisation

### context
- **request_family**: LAND_SEARCH
- **property_type**: terrain_titre
- **transaction_type**: BUY
- **requester_profile**: particulier

### initial_message
"Je cherche un terrain viabilisé à Yaoundé avec eau et électricité déjà au pied."

### extracted_facts
- FLD-TRANSACTION: BUY
- FLD-PROPERTY_TYPE: terrain_titre
- FLD-CITY: Yaoundé
- FLD-VIABILISE: OUI
- FLD-EAU: OUI
- FLD-ELECTRICITE: OUI

### missing_fields (ordered by priority)
1. FLD-BUDGET_MAX — Budget non mentionné
2. FLD-SURFACE — Surface recherchée
3. FLD-NEIGHBORHOOD — Quartier non mentionné
4. FLD-VOIRIE — Route goudronnée ?
5. FLD-ASSAINISSEMENT — Tout-à-l'égout ?

### next_question
"Un terrain viabilisé (eau + électricité) à Yaoundé. Quelle surface et quel budget ?"

### readiness_level
INTENT_IDENTIFIED

### allowed_actions
- Demander surface et budget
- Préciser les besoins de viabilisation
- Proposer des terrains prêts à construire

### forbidden_actions
- Proposer des terrains non viabilisés
- Ignorer les réseaux disponibles

### matching_criteria
- FLD-CITY: hard_constraint + weight 25
- FLD-VIABILISE: hard_constraint + weight 25

---
