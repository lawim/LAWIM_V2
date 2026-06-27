# LAWIM

# 04-MATCHING-REFERENCE.md

## Référentiel Officiel du Moteur de Matching

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit le fonctionnement officiel du moteur de matching de LAWIM.

Il constitue la seule référence autorisée concernant :

* le matching ;
* le rematching ;
* le classement des biens ;
* les recommandations ;
* les propositions ;
* les mises en relation.

Toute implémentation logicielle devra respecter intégralement ce document.

---

# CHAPITRE 2 — MISSION

Le moteur de matching a pour mission de trouver, classer et proposer les biens les plus adaptés à un besoin immobilier.

Il ne recherche pas simplement des biens.

Il recherche les meilleures opportunités disponibles pour un demandeur donné, à un instant donné.

---

# CHAPITRE 3 — PRINCIPES FONDAMENTAUX

Le moteur respecte toujours les principes suivants.

## Principe 1

Le matching commence dès que les champs critiques du type de bien sont connus.

Il n'attend jamais la qualification complète.

---

## Principe 2

Le matching est dynamique.

Chaque nouvelle information peut modifier les résultats.

---

## Principe 3

Le matching est permanent.

Il continue tant que le dossier reste actif.

---

## Principe 4

Le matching apprend des décisions des utilisateurs.

Chaque acceptation ou refus améliore les propositions suivantes.

---

## Principe 5

Le matching privilégie toujours la satisfaction du demandeur.

Il ne cherche pas à proposer le plus grand nombre de biens.

Il cherche à proposer les meilleurs.

---

# CHAPITRE 4 — ÉLÉMENTS PRIS EN COMPTE

Le moteur peut utiliser notamment :

* le type de bien ;
* l'opération ;
* la localisation ;
* le budget ;
* les caractéristiques obligatoires ;
* les caractéristiques recommandées ;
* les préférences exprimées ;
* l'historique du dossier ;
* les refus précédents ;
* les disponibilités du bien ;
* le cycle de vie du bien.

Chaque critère possède une pondération.

---

# CHAPITRE 5 — SOURCES D'INFORMATION

Le matching utilise exclusivement :

* le dossier qualifié ;
* les biens publiés ;
* le référentiel des biens ;
* le catalogue des attributs ;
* les règles de cohérence.

Aucune donnée non validée ne participe au calcul.

---

# CHAPITRE 6 — DÉCLENCHEMENT

Le matching est déclenché automatiquement :

* lors de la création d'un dossier ;
* après une correction ;
* après une modification du budget ;
* après un changement de ville ;
* après un changement de type de bien ;
* lors de la publication d'un nouveau bien ;
* lorsqu'un bien devient disponible ;
* après un refus ;
* après une visite ;
* après une négociation échouée.

Aucune action manuelle n'est nécessaire.

---

# CHAPITRE 7 — OBJECTIF FINAL

Le moteur de matching ne s'arrête pas lorsqu'un premier bien est trouvé.

Il poursuit son travail jusqu'à la résolution du dossier.

Le succès du matching est mesuré par :

* la satisfaction des deux parties ;
* la qualité de la mise en relation ;
* la réussite de la transaction ;

et non par le nombre de biens proposés.

---

# FIN DE LA PARTIE 1

# LAWIM

# 04-MATCHING-REFERENCE.md

# PARTIE 2

# Qualification du matching et calcul de la compatibilité

Version 1.0

---

# CHAPITRE 8 — LE MATCHING N'EST PAS UNE RECHERCHE SQL

Le moteur de matching ne compare jamais simplement deux listes de critères.

Il réalise une évaluation intelligente de la compatibilité entre :

* un dossier de recherche ;
* un bien immobilier.

Le matching est donc un processus décisionnel et non une simple recherche dans une base de données.

---

# CHAPITRE 9 — LES QUATRE NIVEAUX DE COMPATIBILITÉ

Chaque bien est évalué selon quatre niveaux.

## Niveau 1 — Compatibilité critique

Correspond aux champs critiques définis dans :

02-PROPERTY-REFERENCE.md

Sans compatibilité critique, aucun matching n'est possible.

---

## Niveau 2 — Compatibilité fonctionnelle

Le bien répond correctement aux besoins principaux.

Exemple :

* nombre de chambres ;
* superficie ;
* budget ;
* type de bien.

---

## Niveau 3 — Compatibilité de confort

Le bien possède des éléments appréciés mais non indispensables.

Exemple :

* garage ;
* forage ;
* jardin ;
* piscine ;
* balcon ;
* terrasse.

Ces critères améliorent le score mais ne doivent jamais éliminer un bien compatible.

---

## Niveau 4 — Compatibilité préférentielle

Le moteur tient compte des préférences observées.

Exemple :

quartier préféré ;

orientation ;

vue ;

proximité école ;

proximité travail ;

habitudes du demandeur.

Ces critères servent principalement à classer les biens.

---

# CHAPITRE 10 — SCORE DE COMPATIBILITÉ

Chaque bien reçoit un score global compris entre :

0 %

et

100 %.

Le score est calculé exclusivement à partir des règles métier.

Le score doit être explicable.

LAWIM doit toujours être capable de justifier pourquoi un bien a obtenu un meilleur score qu'un autre.

---

# CHAPITRE 11 — CHAMPS ÉLIMINATOIRES

Certains critères sont obligatoires.

Exemple :

Le demandeur cherche :

Appartement.

↓

Le moteur ne propose jamais :

Terrain.

---

Autre exemple.

Location.

↓

Le moteur ne propose jamais :

Vente.

---

Autre exemple.

Budget maximal :

30 millions.

↓

Le moteur ne propose pas volontairement un bien à 90 millions.

---

Ces critères sont dits éliminatoires.

---

# CHAPITRE 12 — CHAMPS FLEXIBLES

Certains critères peuvent être assouplis progressivement.

Exemples :

* superficie ;
* distance ;
* quartier ;
* équipements ;
* confort.

Le moteur élargit progressivement la recherche si nécessaire.

Cette stratégie est entièrement automatique.

---

# CHAPITRE 13 — BUDGET

Le budget constitue un critère majeur.

Le moteur distingue notamment :

* budget maximal ;
* budget minimal ;
* marge de négociation.

Le moteur peut proposer un bien légèrement supérieur au budget uniquement lorsque :

* les autres critères sont excellents ;
* ou lorsque le demandeur a déjà accepté des biens comparables.

Cette proposition doit être clairement justifiée.

---

# CHAPITRE 14 — LOCALISATION

La localisation est évaluée selon plusieurs niveaux.

* ville ;
* arrondissement ;
* quartier ;
* secteur ;
* proximité.

Lorsque le quartier demandé ne contient aucun bien compatible.

Le moteur peut proposer des quartiers voisins présentant des caractéristiques similaires.

La proposition doit toujours être expliquée.

---

# CHAPITRE 15 — DISTANCE

Lorsque les coordonnées GPS sont disponibles.

Le moteur utilise la distance réelle.

Il ne se limite pas au nom du quartier.

Il privilégie les trajets pertinents plutôt que la distance à vol d'oiseau.

---

# CHAPITRE 16 — DISPONIBILITÉ

Un bien indisponible ne participe pas au matching.

Exemples :

* vendu ;
* loué ;
* suspendu ;
* archivé.

Les biens disponibles sont prioritaires.

---

# CHAPITRE 17 — QUALITÉ DES DONNÉES

Deux biens identiques peuvent recevoir des scores différents.

Le moteur favorise :

* les biens complètement qualifiés ;
* les biens géolocalisés ;
* les biens avec photos ;
* les biens récemment mis à jour.

Ces critères n'améliorent pas la compatibilité mais augmentent la confiance.

---

# CHAPITRE 18 — FRAÎCHEUR DU BIEN

Le moteur tient compte de l'activité récente.

Exemples :

* publication récente ;
* disponibilité confirmée ;
* propriétaire actif.

Les biens inactifs perdent progressivement en priorité.

---

# CHAPITRE 19 — HISTORIQUE DU DEMANDEUR

Le moteur apprend.

Exemples :

Trois refus pour absence de garage.

↓

Le garage devient prioritaire.

---

Acceptation répétée d'un quartier.

↓

Ce quartier est favorisé.

---

Le système apprend uniquement à partir des décisions réellement prises.

---

# CHAPITRE 20 — HISTORIQUE DU DÉTENTEUR

Le moteur tient également compte du comportement du détenteur.

Exemples :

* délai moyen de réponse ;
* taux d'acceptation ;
* disponibilité réelle ;
* fiabilité.

Les détenteurs fiables sont privilégiés.

---

# CHAPITRE 21 — MATCHING MULTI-BIENS

Un dossier peut correspondre à plusieurs biens.

Le moteur ne cherche pas un unique résultat.

Il produit un classement.

Ce classement évolue continuellement.

---

# CHAPITRE 22 — JUSTIFICATION

Chaque proposition doit être justifiable.

Exemple :

🏠 Cette villa est proposée parce qu'elle :

• respecte votre budget ;

• possède quatre chambres ;

• est située à Bastos ;

• dispose d'un garage ;

• est disponible immédiatement.

L'utilisateur doit comprendre immédiatement pourquoi ce bien lui est présenté.

---

# CHAPITRE 23 — OBJECTIF FINAL

Le moteur ne cherche pas uniquement à maximiser un score.

Il cherche à maximiser la probabilité qu'une transaction aboutisse.

Toutes les décisions du moteur doivent tendre vers cet objectif.

---

# FIN DE LA PARTIE 2


# 04-MATCHING-REFERENCE.md

# PARTIE 3

# Algorithme officiel de Matching

Version 1.0

---

# CHAPITRE 24 — ALGORITHME GÉNÉRAL

Pour chaque dossier actif, le moteur exécute obligatoirement l'algorithme suivant.

```
1. Charger le dossier

↓

2. Vérifier les champs critiques

↓

3. Sélectionner les biens compatibles

↓

4. Éliminer les biens incompatibles

↓

5. Calculer les scores

↓

6. Classer les biens

↓

7. Proposer les meilleurs

↓

8. Attendre la décision

↓

9. Apprendre

↓

10. Recalculer si nécessaire
```

---

# CHAPITRE 25 — FILTRE ÉLIMINATOIRE

Avant tout calcul.

Tous les biens incompatibles sont supprimés.

Exemple

Appartement

↓

Terrain

↓

Éliminé.

---

Location

↓

Vente

↓

Éliminé.

---

Villa

↓

Studio

↓

Éliminé.

---

Budget maximum

50 M

↓

Bien

120 M

↓

Éliminé (sauf si dépassement autorisé).

---

# CHAPITRE 26 — SCORE IMMOBILIER

Le score immobilier est calculé comme suit.

| Critère                       | Poids |
| ----------------------------- | ----: |
| Type de bien                  |  25 % |
| Opération                     |  20 % |
| Budget                        |  15 % |
| Localisation                  |  15 % |
| Caractéristiques critiques    |  15 % |
| Caractéristiques recommandées |  10 % |

Si le score est inférieur à **60 %**, le bien n'est jamais proposé.

---

# CHAPITRE 27 — SCORE GÉOGRAPHIQUE

Le score géographique tient compte :

* ville ;
* quartier ;
* GPS ;
* distance réelle ;
* temps de trajet.

Lorsque les coordonnées GPS sont disponibles.

Le calcul s'effectue à partir des coordonnées GPS.

Sinon.

La localisation administrative est utilisée.

---

# CHAPITRE 28 — SCORE DISPONIBILITÉ

Le bien reçoit un score de disponibilité.

100 %

Disponible.

---

70 %

Réservation en cours.

---

30 %

Réponse propriétaire en attente.

---

0 %

Vendu.

Loué.

Archivé.

Les biens à 0 % ne sont jamais proposés.

---

# CHAPITRE 29 — SCORE DOCUMENTAIRE

Les documents améliorent le score.

Exemple

Titre foncier

100 %

---

En cours d'immatriculation

80 %

---

Droit coutumier

60 %

---

Documents inconnus

40 %

---

# CHAPITRE 30 — SCORE QUALITÉ

Le moteur favorise les annonces complètes.

Points attribués pour :

* photos ;
* GPS ;
* description ;
* qualification complète ;
* disponibilité confirmée.

---

# CHAPITRE 31 — SCORE DÉTENTEUR

Le moteur calcule automatiquement un indice de fiabilité.

Exemple

Temps moyen de réponse

*

Taux d'acceptation

*

Visites honorées

*

Transactions conclues

↓

Indice de fiabilité.

Cet indice influence uniquement le classement.

Jamais l'éligibilité.

---

# CHAPITRE 32 — SCORE DEMANDEUR

Même principe.

Le moteur observe notamment :

* budget confirmé ;
* téléphone vérifié ;
* visites honorées ;
* réponses rapides.

Ce score sert uniquement à estimer la probabilité de succès.

---

# CHAPITRE 33 — SCORE GLOBAL

Le score final est calculé.

```
Score Immobilier

+

Score Géographique

+

Disponibilité

+

Documents

+

Qualité

+

Fiabilité détenteur

+

Probabilité de transaction

↓

Score global
```

Le score est compris entre :

0

et

100.

---

# CHAPITRE 34 — CLASSEMENT

Tous les biens sont triés.

Ordre décroissant.

Le moteur ne propose jamais plus de :

5 biens

lors d'un premier matching.

Les autres restent en attente.

---

# CHAPITRE 35 — EXPLICATION

Chaque proposition doit pouvoir être expliquée.

Exemple

🏠 Villa

Score

94 %

Pourquoi ?

✓ budget respecté

✓ Bastos

✓ 4 chambres

✓ garage

✓ propriétaire réactif

✓ disponible immédiatement

Le moteur ne présente jamais un score sans justification.

---

# CHAPITRE 36 — APPRENTISSAGE

Après chaque décision.

Le moteur met à jour :

* préférences ;
* refus ;
* acceptations ;
* historique.

Ces informations servent au matching suivant.

---

# CHAPITRE 37 — REMATCHING

Le rematching est automatique.

Il est déclenché notamment lorsque :

* un bien disparaît ;
* un propriétaire refuse ;
* une visite échoue ;
* une négociation échoue ;
* un nouveau bien est publié.

Le dossier est immédiatement recalculé.

---

# CHAPITRE 38 — RÈGLES D'OR

Le moteur ne doit jamais :

❌ proposer un bien incompatible ;

❌ proposer un bien vendu ;

❌ proposer deux fois le même bien après un refus définitif ;

❌ ignorer les préférences apprises ;

❌ recalculer inutilement les scores.

---

# CHAPITRE 39 — OBJECTIF FINAL

Le moteur poursuit le matching jusqu'à ce que :

* une transaction soit réalisée ;

ou

* le dossier soit clôturé.

Le premier bien trouvé n'est jamais considéré comme le résultat final.

Le moteur continue à surveiller le marché pendant toute la durée de vie du dossier.

# FIN DE LA PARTIE 3


# 04-MATCHING-REFERENCE.md

# PARTIE 4

# Pondération officielle par type de bien

Version 1.0

---

# CHAPITRE 40 — PRINCIPE GÉNÉRAL

Le matching LAWIM n'utilise jamais une pondération unique pour tous les biens.

Chaque type de bien possède ses propres critères importants.

Exemple :

* pour un terrain, la superficie et la situation juridique sont très importantes ;
* pour un studio, le quartier, le budget et la douche interne sont plus importants ;
* pour une villa, les chambres, la cour, la clôture et les dépendances sont structurantes ;
* pour un hôtel, le nombre de chambres et l'état d'exploitation sont déterminants.

Le moteur doit donc appliquer une pondération adaptée au type de bien.

---

# CHAPITRE 41 — RÈGLE DE TOTALISATION

Pour chaque type de bien, les pondérations métier doivent totaliser 100 %.

Les critères sont regroupés en cinq familles :

1. Compatibilité de base
2. Localisation
3. Budget / prix
4. Caractéristiques métier
5. Qualité et faisabilité

---

# CHAPITRE 42 — RÉSIDENTIEL INDIVIDUEL SIMPLE

Cette catégorie couvre :

* chambre ;
* chambre moderne ;
* studio ;
* studio meublé.

## Pondération

| Critère                   | Poids |
| ------------------------- | ----: |
| Type exact du bien        |  20 % |
| Opération                 |  10 % |
| Ville / quartier          |  25 % |
| Budget                    |  25 % |
| Douche / cuisine / meublé |  10 % |
| Disponibilité             |   5 % |
| Qualité des informations  |   5 % |

## Règles

Le moteur privilégie :

* la proximité ;
* le budget ;
* la disponibilité ;
* la simplicité d'accès.

Le moteur ne doit jamais pénaliser l'absence d'informations de luxe pour ces biens.

---

# CHAPITRE 43 — APPARTEMENT

## Pondération

| Critère                  | Poids |
| ------------------------ | ----: |
| Type exact du bien       |  15 % |
| Opération                |  10 % |
| Ville / quartier         |  20 % |
| Budget                   |  20 % |
| Nombre de chambres       |  15 % |
| Cuisine / douches        |   8 % |
| Parking / balcon / étage |   5 % |
| Disponibilité            |   4 % |
| Qualité des informations |   3 % |

## Règles

Le nombre de chambres est un critère fort.

Les valeurs autorisées sont :

* 2 chambres ;
* 3 chambres ;
* 4 chambres.

Un appartement avec plus de 4 chambres doit être traité comme cas atypique et peut être proposé uniquement s'il reste cohérent avec le dossier.

Le moteur ne doit jamais utiliser le nombre de pièces.

---

# CHAPITRE 44 — APPARTEMENT MEUBLÉ

## Pondération

| Critère                           | Poids |
| --------------------------------- | ----: |
| Type exact du bien                |  15 % |
| Opération                         |  10 % |
| Ville / quartier                  |  18 % |
| Budget                            |  18 % |
| Nombre de chambres                |  12 % |
| Qualité du mobilier / équipements |  12 % |
| Durée souhaitée                   |   5 % |
| Disponibilité                     |   5 % |
| Qualité des informations          |   5 % |

## Règles

Les équipements ont plus de poids que dans un appartement non meublé.

Le moteur tient compte notamment :

* climatisation ;
* internet ;
* cuisine équipée ;
* ménage ;
* sécurité ;
* parking.

---

# CHAPITRE 45 — MAISON

## Pondération

| Critère                       | Poids |
| ----------------------------- | ----: |
| Type exact du bien            |  15 % |
| Opération                     |  10 % |
| Ville / quartier              |  18 % |
| Budget                        |  18 % |
| Nombre de chambres            |  15 % |
| Cour / clôture                |  10 % |
| Douches / cuisine             |   6 % |
| Parking / forage / dépendance |   5 % |
| Qualité des informations      |   3 % |

## Règles

Une maison est évaluée selon sa capacité familiale.

Le moteur privilégie :

* chambres ;
* cour ;
* clôture ;
* accessibilité ;
* budget.

---

# CHAPITRE 46 — VILLA

## Pondération

| Critère                                | Poids |
| -------------------------------------- | ----: |
| Type exact du bien                     |  12 % |
| Opération                              |   8 % |
| Ville / quartier                       |  18 % |
| Budget                                 |  17 % |
| Nombre de chambres                     |  15 % |
| Cour / clôture / barrière              |  10 % |
| Dépendance / garage                    |   8 % |
| Forage / sécurité / groupe électrogène |   5 % |
| Piscine / jardin / confort supérieur   |   4 % |
| Qualité des informations               |   3 % |

## Règles

Une villa doit généralement comporter :

* au moins 4 chambres ;
* une cour ;
* une clôture ou barrière.

Une villa de moins de 4 chambres doit être reclassée ou signalée comme atypique.

Le standing ne doit pas être demandé systématiquement.

Il est déduit des équipements, de la localisation et de la description.

---

# CHAPITRE 47 — DUPLEX

## Pondération

| Critère                     | Poids |
| --------------------------- | ----: |
| Type exact du bien          |  15 % |
| Opération                   |   8 % |
| Ville / quartier            |  18 % |
| Budget                      |  17 % |
| Nombre de chambres          |  12 % |
| Deux niveaux confirmés      |  12 % |
| Cour / parking / dépendance |   8 % |
| Équipements complémentaires |   5 % |
| Qualité des informations    |   5 % |

## Règles

Le critère "deux niveaux" est obligatoire pour confirmer le type duplex.

Sans cette caractéristique, le moteur doit proposer un reclassement vers maison ou villa.

---

# CHAPITRE 48 — IMMEUBLE RÉSIDENTIEL / MINI-CITÉ

## Pondération

| Critère                  | Poids |
| ------------------------ | ----: |
| Type exact               |  15 % |
| Ville / quartier         |  15 % |
| Prix                     |  15 % |
| Nombre d'unités          |  15 % |
| Type d'unités            |  10 % |
| Revenus locatifs         |  12 % |
| Taux d'occupation        |   8 % |
| Documents / titre        |   5 % |
| Qualité des informations |   5 % |

## Règles

Ces biens sont évalués comme biens d'investissement.

Le moteur privilégie :

* revenus locatifs ;
* occupation ;
* état général ;
* fiabilité documentaire.

---

# CHAPITRE 49 — TERRAIN RÉSIDENTIEL / PARCELLE

## Pondération

| Critère                        | Poids |
| ------------------------------ | ----: |
| Type exact du terrain          |  15 % |
| Opération                      |   8 % |
| Ville / zone                   |  18 % |
| Prix / budget                  |  17 % |
| Superficie                     |  15 % |
| Situation juridique            |  12 % |
| Accès / distance axe principal |   7 % |
| Eau / électricité proches      |   4 % |
| GPS / bornage / qualité info   |   4 % |

## Règles

Pour les terrains, la situation juridique est fortement pondérée.

Un terrain avec titre foncier ou document fiable est mieux classé.

Le moteur ne doit jamais utiliser :

* chambres ;
* douches ;
* salon ;
* pièces ;
* standing.

---

# CHAPITRE 50 — TERRAIN AGRICOLE

## Pondération

| Critère                  | Poids |
| ------------------------ | ----: |
| Type exact               |  15 % |
| Localité                 |  15 % |
| Prix                     |  15 % |
| Superficie               |  20 % |
| Situation juridique      |  12 % |
| Activité agricole prévue |   8 % |
| Accès / eau / relief     |   8 % |
| Qualité des informations |   7 % |

## Règles

La superficie et l'usage agricole dominent le scoring.

Les équipements résidentiels ne doivent pas influencer positivement le score.

---

# CHAPITRE 51 — TERRAIN COMMERCIAL / INDUSTRIEL

## Pondération

| Critère                     | Poids |
| --------------------------- | ----: |
| Type exact                  |  15 % |
| Zone / axe                  |  18 % |
| Prix                        |  15 % |
| Superficie                  |  15 % |
| Situation juridique         |  10 % |
| Façade / visibilité         |   8 % |
| Accès gros porteurs / route |   8 % |
| Eau / électricité           |   5 % |
| Qualité des informations    |   6 % |

## Règles

Pour un terrain commercial, la visibilité et la façade ont une grande importance.

Pour un terrain industriel, l'accès poids lourds et les réseaux ont une grande importance.

---

# CHAPITRE 52 — BOUTIQUE / KIOSQUE / ÉCHOPPE

## Pondération

| Critère                   | Poids |
| ------------------------- | ----: |
| Type exact                |  15 % |
| Ville / quartier / marché |  25 % |
| Budget                    |  20 % |
| Surface                   |  10 % |
| Position commerciale      |  12 % |
| Disponibilité             |   8 % |
| Électricité / sécurité    |   5 % |
| Qualité des informations  |   5 % |

## Règles

Le moteur privilégie :

* bordure de route ;
* marché ;
* flux client ;
* accessibilité.

Les critères résidentiels sont interdits.

---

# CHAPITRE 53 — BUREAU / CABINET / COWORKING

## Pondération

| Critère                  | Poids |
| ------------------------ | ----: |
| Type exact               |  15 % |
| Ville / quartier         |  20 % |
| Budget                   |  20 % |
| Surface                  |  12 % |
| Accessibilité            |  10 % |
| Parking                  |   8 % |
| Internet / climatisation |   5 % |
| Étage / ascenseur        |   5 % |
| Qualité des informations |   5 % |

## Règles

Le moteur privilégie :

* accessibilité ;
* image professionnelle du quartier ;
* parking ;
* internet.

---

# CHAPITRE 54 — ENTREPÔT / HANGAR / DÉPÔT

## Pondération

| Critère                  | Poids |
| ------------------------ | ----: |
| Type exact               |  15 % |
| Zone                     |  15 % |
| Budget                   |  15 % |
| Surface                  |  20 % |
| Accès camion             |  12 % |
| Hauteur / quai           |   8 % |
| Sécurité / clôture       |   6 % |
| Électricité / eau        |   4 % |
| Qualité des informations |   5 % |

## Règles

Le moteur privilégie :

* surface ;
* accès camion ;
* hauteur utile ;
* sécurité.

---

# CHAPITRE 55 — HÔTEL / AUBERGE / MOTEL / RÉSIDENCE HÔTELIÈRE

## Pondération

| Critère                         | Poids |
| ------------------------------- | ----: |
| Type exact                      |  12 % |
| Ville / quartier / axe          |  15 % |
| Prix                            |  15 % |
| Nombre de chambres / unités     |  18 % |
| État d'exploitation             |  10 % |
| Taux d'occupation / revenus     |  10 % |
| Parking / restaurant / services |   8 % |
| Documents / autorisations       |   5 % |
| Qualité des informations        |   7 % |

## Règles

Ces biens sont évalués à la fois comme biens immobiliers et comme activités économiques.

La capacité d'exploitation est essentielle.

---

# CHAPITRE 56 — BIENS AGRICOLES

## Pondération

| Critère                  | Poids |
| ------------------------ | ----: |
| Type exact               |  15 % |
| Localité                 |  15 % |
| Prix                     |  15 % |
| Superficie               |  20 % |
| Activité principale      |  10 % |
| Situation juridique      |  10 % |
| Eau / accès / fertilité  |   8 % |
| Équipements / bâtiments  |   4 % |
| Qualité des informations |   3 % |

## Règles

Le moteur privilégie :

* superficie ;
* activité principale ;
* eau ;
* accès ;
* situation juridique.

---

# CHAPITRE 57 — BIENS INDUSTRIELS ET LOGISTIQUES

## Pondération

| Critère                          | Poids |
| -------------------------------- | ----: |
| Type exact                       |  15 % |
| Zone industrielle / localisation |  15 % |
| Prix                             |  15 % |
| Surface                          |  18 % |
| Accessibilité poids lourds       |  12 % |
| Énergie / eau                    |   8 % |
| État général                     |   7 % |
| Équipements techniques           |   5 % |
| Qualité des informations         |   5 % |

## Règles

Les critères résidentiels sont interdits.

Le moteur privilégie les biens immédiatement exploitables.

---

# CHAPITRE 58 — BIENS MIXTES ET SPÉCIAUX

## Pondération

| Critère                            | Poids |
| ---------------------------------- | ----: |
| Usage principal                    |  20 % |
| Usage secondaire                   |   8 % |
| Ville / quartier                   |  15 % |
| Prix                               |  15 % |
| Surface                            |  12 % |
| Revenus ou capacité d'exploitation |  10 % |
| Accessibilité                      |   8 % |
| Documents / autorisations          |   6 % |
| Qualité des informations           |   6 % |

## Règles

Le moteur évalue d'abord l'usage principal.

Les usages secondaires améliorent le score, mais ne doivent pas masquer l'usage dominant.

---

# CHAPITRE 59 — RÈGLE D'AJUSTEMENT PAR APPRENTISSAGE

Les pondérations ci-dessus constituent les valeurs de départ.

Le moteur peut ajuster le classement d'un dossier à partir des comportements observés.

Exemple :

Si un demandeur refuse plusieurs biens sans parking, le parking devient plus important dans ce dossier.

Si un demandeur accepte plusieurs biens hors quartier initial, la contrainte de quartier devient plus flexible.

Ces ajustements sont propres au dossier.

Ils ne modifient pas le référentiel global.

---

# CHAPITRE 60 — RÈGLE D'EXPLICATION

Le moteur doit pouvoir expliquer les trois premiers critères ayant le plus influencé chaque proposition.

Exemple :

Cette villa est proposée principalement parce que :

• elle respecte votre budget ;

• elle se trouve dans le quartier recherché ;

• elle possède les 4 chambres demandées.

Le moteur ne doit jamais présenter un bien sans justification.

---

# CHAPITRE 61 — RÈGLE DE NON-COMPENSATION

Certains critères ne peuvent pas compenser une incompatibilité majeure.

Exemple :

Un terrain très bien situé ne compense jamais le fait que l'utilisateur cherche une villa.

Une villa avec piscine ne compense jamais un budget totalement incompatible.

Un hôtel très rentable ne compense jamais l'absence de disponibilité à la vente si l'opération demandée est achat.

---

# CHAPITRE 62 — OBJECTIF DE CETTE PARTIE

Cette partie définit les pondérations de départ du moteur de matching.

Elles doivent être implémentées comme règles métier configurables.

Elles ne doivent jamais être dispersées dans le code.

Toute modification d'une pondération doit être documentée ici avant d'être appliquée.

---

# FIN DE LA PARTIE 4

# 04-MATCHING-REFERENCE.md

# PARTIE 5

# Rematching intelligent, apprentissage continu et optimisation dynamique

Version 1.0

---

# CHAPITRE 63 — PRINCIPE FONDAMENTAL

Dans LAWIM, un matching n'est jamais définitif.

Chaque dossier est considéré comme vivant.

Le moteur réévalue continuellement les opportunités jusqu'à la clôture du dossier.

Le rematching constitue donc le fonctionnement normal du système.

---

# CHAPITRE 64 — DÉFINITION DU REMATCHING

Le rematching consiste à recalculer automatiquement les meilleures propositions disponibles à partir :

* des nouvelles informations du dossier ;
* des nouvelles informations sur les biens ;
* des décisions des utilisateurs ;
* des évolutions du marché.

Le rematching ne remet jamais le dossier à zéro.

Il enrichit progressivement la qualité des propositions.

---

# CHAPITRE 65 — ÉVÉNEMENTS DÉCLENCHEURS

Le moteur lance automatiquement un rematching lorsqu'un des événements suivants survient :

## Côté demandeur

* modification du budget ;
* changement de ville ;
* changement de quartier ;
* changement de type de bien ;
* ajout d'un nouveau critère ;
* suppression d'un critère ;
* refus d'un bien ;
* abandon d'une visite ;
* nouvelle préférence exprimée.

---

## Côté bien

* publication ;
* modification ;
* baisse du prix ;
* hausse du prix ;
* changement de disponibilité ;
* ajout de photos ;
* ajout des coordonnées GPS ;
* ajout des documents ;
* amélioration de la qualification.

---

## Côté détenteur

* acceptation ;
* refus ;
* absence de réponse ;
* indisponibilité temporaire ;
* retour en disponibilité.

---

## Côté système

* nouvelle règle métier ;
* recalcul périodique ;
* apprentissage global ;
* correction des données.

---

# CHAPITRE 66 — REMATCHING SÉLECTIF

Le moteur ne recalcule jamais inutilement toute la base.

Il identifie uniquement les dossiers concernés.

Exemple

Publication d'une villa à Bastos.

↓

Recalcul uniquement :

* dossiers recherchant une villa ;
* à Yaoundé ;
* compatibles avec Bastos.

Les autres dossiers restent inchangés.

---

# CHAPITRE 67 — REMATCHING GÉOGRAPHIQUE

Lorsqu'un nouveau bien apparaît.

Le moteur calcule automatiquement :

* les distances GPS ;
* les temps estimés ;
* les zones voisines ;
* les quartiers limitrophes.

Il peut proposer un quartier voisin si celui-ci offre une meilleure probabilité de réussite.

---

# CHAPITRE 68 — REMATCHING PAR APPRENTISSAGE

Le moteur apprend des comportements.

Exemple

Le demandeur refuse successivement :

* Bonamoussadi ;
* Logbessou ;
* PK13.

Le moteur détecte une préférence implicite.

Les quartiers similaires deviennent moins prioritaires.

Inversement.

Les quartiers régulièrement acceptés gagnent automatiquement en importance.

---

# CHAPITRE 69 — REMATCHING PAR NÉGOCIATION

Lorsqu'un prix est modifié.

Le moteur recalcule immédiatement.

Exemple

Prix initial

75 M

↓

Nouveau prix

68 M

↓

Le bien peut désormais entrer dans plusieurs nouveaux dossiers.

Tous ces dossiers sont automatiquement recalculés.

---

# CHAPITRE 70 — REMATCHING PAR CYCLE DE VIE

Chaque changement de cycle de vie entraîne un recalcul.

Exemple

Créé

↓

Publié

↓

Matching.

---

Publié

↓

Réservé

↓

Suppression des nouvelles propositions.

---

Réservé

↓

Disponible

↓

Réapparition automatique.

---

Vendu

↓

Retrait définitif.

---

# CHAPITRE 71 — BIENS DÉJÀ REFUSÉS

Un bien définitivement refusé n'est jamais reproposé.

Exceptions :

* baisse importante du prix ;
* modification majeure ;
* changement du besoin ;
* demande explicite du demandeur.

---

# CHAPITRE 72 — APPRENTISSAGE DU DOSSIER

Chaque interaction améliore la connaissance du projet.

Le moteur enregistre notamment :

* critères acceptés ;
* critères refusés ;
* quartiers appréciés ;
* budgets réellement acceptés ;
* délais acceptables ;
* préférences implicites.

Ces informations restent propres au dossier.

---

# CHAPITRE 73 — APPRENTISSAGE GLOBAL

LAWIM améliore également son moteur de manière globale.

Exemples

Les appartements meublés à Bonapriso sont très demandés.

↓

Le moteur adapte leur priorité.

---

Les terrains avec titre foncier trouvent rapidement preneur.

↓

Le moteur renforce leur classement.

Cet apprentissage global ne modifie jamais les critères individuels d'un dossier.

---

# CHAPITRE 74 — DÉTECTION DES OPPORTUNITÉS

Le moteur détecte automatiquement les événements favorables.

Exemples

Baisse de prix.

↓

Nouvelle opportunité.

---

Nouveau bien correspondant à 98 %.

↓

Notification immédiate.

---

Retour d'un bien précédemment indisponible.

↓

Rematching.

---

# CHAPITRE 75 — DÉTECTION DES RISQUES

Le moteur détecte également les risques.

Exemples

Bien sans réponse depuis longtemps.

↓

Baisse de priorité.

---

Propriétaire inactif.

↓

Indice de fiabilité réduit.

---

Documents incomplets.

↓

Avertissement.

---

Prix anormalement élevé.

↓

Score de faisabilité diminué.

---

# CHAPITRE 76 — PRIORITÉ DES PROPOSITIONS

Tous les biens compatibles ne sont pas présentés.

Le moteur privilégie :

1. la meilleure probabilité de transaction ;
2. la meilleure compatibilité ;
3. la meilleure disponibilité ;
4. le meilleur niveau documentaire ;
5. la meilleure réactivité du détenteur.

---

# CHAPITRE 77 — ÉQUILIBRE DES PROPOSITIONS

Le moteur évite de proposer plusieurs biens quasiment identiques.

Exemple

Trois appartements dans le même immeuble.

↓

Le moteur en présente un seul en priorité.

Les autres restent disponibles si nécessaire.

Cette règle favorise la diversité des propositions.

---

# CHAPITRE 78 — EXPLICATION DU REMATCHING

Chaque rematching doit être compréhensible.

Exemple

🤖 **LAWIM AI**

Bonne nouvelle.

Une nouvelle villa correspondant davantage à votre budget vient d'être publiée.

Je vous la propose en priorité.

---

Ou

🤖 **LAWIM AI**

Le propriétaire ayant retiré son bien, j'ai automatiquement recherché les meilleures alternatives.

---

# CHAPITRE 79 — SURVEILLANCE CONTINUE

Le moteur surveille en permanence :

* les biens ;
* les dossiers ;
* les disponibilités ;
* les documents ;
* les prix ;
* les réponses des détenteurs ;
* les événements du marché.

Cette surveillance est continue tant que le dossier reste actif.

---

# CHAPITRE 80 — OBJECTIF FINAL

Le rematching ne cherche pas à multiplier les propositions.

Il cherche à améliorer continuellement la probabilité de réussite de la transaction.

Un dossier ne cesse jamais d'être optimisé tant qu'il n'est pas clôturé.

---

# CHAPITRE 81 — RÈGLES IMPÉRATIVES

Le moteur doit obligatoirement :

✓ apprendre de chaque décision ;

✓ réagir immédiatement aux changements significatifs ;

✓ conserver l'historique des propositions ;

✓ éviter les propositions répétitives ;

✓ expliquer chaque nouvelle recommandation ;

✓ privilégier la qualité plutôt que la quantité.

Le moteur ne doit jamais :

❌ repartir de zéro ;

❌ oublier les préférences acquises ;

❌ proposer un bien définitivement écarté sans justification ;

❌ effectuer des recalculs inutiles.

---

# CHAPITRE 82 — CONFORMITÉ

Toute implémentation du moteur de rematching devra respecter strictement les règles définies dans cette partie.

Aucun algorithme de rematching ne pourra être déployé s'il :

* ignore l'apprentissage du dossier ;
* ne tient pas compte des changements de cycle de vie des biens ;
* ne justifie pas les nouvelles propositions ;
* ou ne garantit pas l'amélioration continue de la probabilité de succès de la transaction.

---

# FIN DE LA PARTIE 5


# LAWIM

# 04-MATCHING-REFERENCE.md

# PARTIE 6

# Moteur décisionnel (Decision Engine)

Version 1.0

---

# CHAPITRE 83 — PRINCIPE FONDAMENTAL

Le moteur de matching de LAWIM ne décide jamais uniquement :

> Quel est le meilleur bien ?

Il décide :

> Quelle est la meilleure prochaine action pour maximiser les chances de réussite de la transaction.

Le matching alimente le **Decision Engine**.

---

# CHAPITRE 84 — RÔLE DU DECISION ENGINE

Le Decision Engine est le moteur décisionnel officiel de LAWIM.

Le nom historique `TSE` ne doit plus être utilisé comme appellation officielle.

À chaque événement, il choisit l'action ayant la plus forte valeur ajoutée pour le dossier.

Il ne prend jamais plusieurs décisions contradictoires.

---

# CHAPITRE 85 — ÉVÉNEMENTS ANALYSÉS

Le Decision Engine réagit notamment à :

## Demandeur

* nouveau message ;
* correction ;
* nouveau critère ;
* refus ;
* acceptation ;
* visite ;
* négociation.

---

## Bien

* publication ;
* modification ;
* baisse du prix ;
* retrait ;
* vente ;
* location ;
* nouvelle disponibilité.

---

## Détenteur

* réponse ;
* refus ;
* acceptation ;
* indisponibilité ;
* silence.

---

## Système

* expiration d'un délai ;
* rappel programmé ;
* recalcul périodique ;
* apprentissage.

---

# CHAPITRE 86 — ACTIONS POSSIBLES

Après analyse.

Le moteur choisit UNE action.

Liste officielle.

## Action 1

Poser une question.

---

## Action 2

Lancer un matching.

---

## Action 3

Lancer un rematching.

---

## Action 4

Présenter un bien.

---

## Action 5

Présenter plusieurs biens.

---

## Action 6

Contacter le détenteur.

---

## Action 7

Organiser une visite.

---

## Action 8

Programmer une relance.

---

## Action 9

Notifier.

---

## Action 10

Ouvrir une négociation.

---

## Action 11

Demander un document.

---

## Action 12

Clôturer le dossier.

---

Aucune autre action n'est autorisée.

---

# CHAPITRE 87 — MATRICE DE DÉCISION

Le moteur applique toujours la logique suivante.

```text
Champs critiques manquants

↓

Question

--------------------

Matching impossible

↓

Qualification

--------------------

Matching disponible

↓

Calcul des scores

--------------------

Excellent bien trouvé

↓

Présentation

--------------------

Bien accepté

↓

Contact détenteur

--------------------

Double accord

↓

Visite

--------------------

Visite réussie

↓

Négociation

--------------------

Accord

↓

Transaction

--------------------

Transaction terminée

↓

Clôture
```

---

# CHAPITRE 88 — PRIORITÉ DES ACTIONS

Lorsque plusieurs actions sont possibles.

Le moteur applique l'ordre suivant.

| Priorité | Action                      |
| -------- | --------------------------- |
| 1        | Corriger une incohérence    |
| 2        | Compléter un champ critique |
| 3        | Matching                    |
| 4        | Présenter un bien           |
| 5        | Contacter le détenteur      |
| 6        | Organiser une visite        |
| 7        | Relancer                    |
| 8        | Notifications               |
| 9        | Optimisation du dossier     |

Une seule action principale est exécutée à la fois.

---

# CHAPITRE 89 — SCORE DE SUCCÈS DE TRANSACTION

Chaque couple :

Demandeur

↓

Bien

↓

Détenteur

reçoit un **Transaction Success Score**.

Ce score représente la probabilité de réussite de la transaction.

Il est compris entre :

0 %

et

100 %.

---

# CHAPITRE 90 — COMPOSITION DU SCORE

Le score final est obtenu par la combinaison des indicateurs suivants.

| Indicateur                 | Poids |
| -------------------------- | ----: |
| Compatibilité immobilière  |  30 % |
| Compatibilité géographique |  15 % |
| Disponibilité réelle       |  10 % |
| Situation documentaire     |  10 % |
| Réactivité du détenteur    |  10 % |
| Historique du demandeur    |  10 % |
| Faisabilité financière     |  10 % |
| Probabilité de négociation |   5 % |

Ces valeurs constituent les pondérations par défaut.

Elles peuvent être ajustées uniquement par évolution officielle du référentiel.

---

# CHAPITRE 91 — INDICE DE CONFIANCE

En complément du score.

Chaque proposition reçoit un indice de confiance.

Exemple

Très élevé

Élevé

Moyen

Faible

Très faible

Cet indice mesure la qualité des informations utilisées.

Exemple :

* GPS confirmé ;
* documents vérifiés ;
* disponibilité récente ;
* propriétaire actif.

---

# CHAPITRE 92 — DÉCISION AUTOMATIQUE

Le moteur choisit automatiquement.

Exemple.

Score

98 %

↓

Présenter immédiatement.

---

Score

82 %

↓

Présenter si aucun meilleur bien.

---

Score

55 %

↓

Conserver en attente.

---

Score

25 %

↓

Ne jamais proposer.

---

# CHAPITRE 93 — DÉTECTION DES OPPORTUNITÉS

Le moteur identifie automatiquement :

* baisse importante du prix ;
* nouveau bien très compatible ;
* retour en disponibilité ;
* amélioration documentaire ;
* amélioration du score.

Ces événements déclenchent des actions automatiques.

---

# CHAPITRE 94 — DÉTECTION DES RISQUES

Le moteur surveille :

* propriétaire inactif ;
* délais anormaux ;
* documents incomplets ;
* prix incohérent ;
* bien ancien sans activité.

Le score de confiance est ajusté.

---

# CHAPITRE 95 — MÉMOIRE DU MARCHÉ

LAWIM construit progressivement une connaissance du marché.

Par exemple :

* délai moyen de vente par ville ;
* délai moyen de location ;
* durée moyenne avant première visite ;
* quartiers les plus demandés ;
* types de biens les plus recherchés ;
* saisonnalité.

Ces données servent uniquement à améliorer les décisions.

Elles ne remplacent jamais les critères du dossier.

---

# CHAPITRE 96 — INDICE DE TENSION DU MARCHÉ

Pour chaque combinaison :

Ville

↓

Quartier

↓

Type de bien

↓

Opération

LAWIM calcule un indice de tension.

Exemple.

95 %

Marché très tendu.

↓

Les biens sont rares.

---

25 %

Marché détendu.

↓

Beaucoup de biens disponibles.

Le moteur adapte alors ses recommandations.

---

# CHAPITRE 97 — IA DE NÉGOCIATION

LAWIM peut assister la négociation.

Exemple.

Prix demandé

80 M

↓

Budget

77 M

↓

Écart

3 M

Le moteur peut signaler :

> La probabilité d'un accord est élevée.

Il ne prend jamais la décision à la place des parties.

---

# CHAPITRE 98 — OPTIMISATION CONTINUE

Le moteur réévalue chaque dossier :

* après chaque événement important ;
* lors de chaque rematching ;
* lors de chaque nouvelle publication ;
* lors des recalculs périodiques.

Aucun dossier actif n'est oublié.

---

# CHAPITRE 99 — RÈGLES ABSOLUES

Le Decision Engine doit toujours :

✓ privilégier la transaction la plus probable ;

✓ expliquer ses décisions importantes ;

✓ apprendre de chaque interaction ;

✓ conserver la traçabilité complète ;

✓ respecter les référentiels officiels.

Il ne doit jamais :

❌ privilégier un partenaire au détriment du demandeur ;

❌ masquer une information importante ;

❌ proposer un bien incompatible ;

❌ ignorer le cycle de vie d'un bien ;

❌ prendre une décision sans justification métier.

---

# CHAPITRE 100 — OBJECTIF FINAL

Le Decision Engine constitue le cerveau décisionnel de LAWIM.

Son objectif n'est pas de trouver le plus grand nombre de biens.

Son objectif est de conduire chaque dossier jusqu'à une transaction réussie dans les meilleures conditions possibles.

Toutes les décisions du moteur doivent contribuer à :

* améliorer l'expérience utilisateur ;
* réduire les délais ;
* augmenter le taux de réussite des transactions ;
* renforcer la confiance entre toutes les parties.

---

# FIN DE LA PARTIE 6

## FIN DU DOCUMENT

Le présent **04-MATCHING-REFERENCE.md** constitue le référentiel officiel du moteur de matching et du moteur décisionnel de LAWIM.

Toute implémentation (backend, IA, API, application mobile ou web) devra appliquer strictement les règles définies dans ce document.

Toute logique de matching, de scoring, de rematching ou de décision non conforme à ce référentiel est interdite et devra être supprimée.

