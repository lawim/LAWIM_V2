# LAWIM

# CONSTITUTION OFFICIELLE

## Version 1.0

---

# PRÉAMBULE

La présente Constitution constitue la référence fonctionnelle officielle de LAWIM.

Elle définit l'ensemble des règles métier qui gouvernent la plateforme.

À compter de son adoption, **aucune règle métier ne peut exister en dehors de cette Constitution**.

Le code informatique n'est qu'une implémentation de cette Constitution.

En cas de contradiction entre le code et la Constitution, **la Constitution prévaut toujours**.

---

# ARTICLE 1 — MISSION DE LAWIM

LAWIM est une plateforme immobilière intelligente destinée principalement au marché camerounais, tout en restant compatible avec les standards internationaux.

Sa mission est de faciliter, sécuriser et accélérer :

* la recherche de biens ;
* la publication de biens ;
* la mise en relation entre les parties ;
* la qualification des besoins ;
* le matching intelligent ;
* la négociation ;
* la transaction ;
* le suivi de la relation.

LAWIM accompagne l'utilisateur jusqu'à la résolution complète de son besoin immobilier.

LAWIM finance son activité par les services LAWIM et la mise en relation payante, sans prélever de commission sur les ventes ou locations immobilières.

---

# ARTICLE 2 — OBJECTIFS

LAWIM poursuit les objectifs suivants.

## 2.1

Comprendre le besoin réel de l'utilisateur.

## 2.2

Collecter uniquement les informations utiles.

## 2.3

Éviter toute question inutile.

## 2.4

Réduire le nombre de messages nécessaires.

## 2.5

Trouver le meilleur bien disponible.

## 2.6

Mettre en relation les bonnes personnes.

## 2.7

Assurer le suivi jusqu'à la conclusion du dossier.

## 2.8

Relancer automatiquement un matching lorsqu'une proposition échoue.

---

# ARTICLE 3 — PHILOSOPHIE DE LAWIM

LAWIM n'est pas un simple catalogue d'annonces.

LAWIM est un assistant immobilier intelligent.

La plateforme doit toujours privilégier :

* la compréhension du besoin ;
* la qualité du matching ;
* la simplicité des échanges ;
* l'efficacité.

Le système ne doit jamais fonctionner comme un formulaire déguisé.

Le dialogue doit rester naturel.

---

# ARTICLE 4 — PRINCIPES FONDATEURS

## Principe 1

Une information déjà donnée ne doit jamais être redemandée.

---

## Principe 2

Une correction utilisateur remplace immédiatement l'information précédente.

Exemple :

Utilisateur :

> Je cherche à Douala.

Puis :

> Finalement Yaoundé.

Le système conserve uniquement :

Ville = Yaoundé.

---

## Principe 3

Le moteur conversationnel ne pose jamais une question dont la réponse peut être déduite.

Exemple :

Si la description indique :

> Villa moderne de cinq chambres avec piscine.

Le système ne demande pas :

* combien de chambres ?
* quel standing ?

Ces informations sont déjà connues ou déductibles.

---

## Principe 4

Le système recherche en permanence les informations critiques dans les messages.

Chaque message utilisateur doit être analysé afin d'extraire automatiquement :

* type de bien ;
* opération ;
* ville ;
* quartier ;
* budget ;
* caractéristiques ;
* contraintes.

---

## Principe 5

Le matching commence dès que les informations critiques sont disponibles.

Les informations facultatives améliorent le score.

Elles ne doivent jamais bloquer le lancement du matching.

---

## Principe 6

La conversation ne suit jamais un questionnaire fixe.

Elle suit uniquement les informations manquantes.

Deux utilisateurs peuvent donc recevoir des questions différentes.

---

## Principe 7

La plateforme doit s'adapter aux usages camerounais.

Les expressions locales sont prioritaires.

Exemples :

* chambre moderne ;
* mini-cité ;
* droit coutumier ;
* titre foncier ;
* chambre avec douche ;
* studio meublé.

---

## Principe 8

La plateforme reste compatible avec les standards internationaux.

Les concepts internationaux sont traduits vers les usages LAWIM.

---

# ARTICLE 5 — SOURCE UNIQUE DE VÉRITÉ

La présente Constitution constitue la seule source officielle des règles métier.

Les documents contenus dans :

```
KNOWLEDGE/CONSTITUTION/
```

font foi.

Les éléments suivants ne doivent jamais contenir une règle métier indépendante :

* services NestJS ;
* contrôleurs ;
* composants React ;
* Prisma ;
* migrations ;
* prompts ;
* dashboards ;
* tests ;
* scripts.

Ils doivent uniquement implémenter les règles définies par la Constitution.

---

# ARTICLE 6 — RÈGLE D'IRRÉVERSIBILITÉ

Toute règle métier contradictoire doit être supprimée.

Il est interdit de :

* conserver une ancienne logique pour compatibilité ;
* commenter une ancienne règle au lieu de la supprimer ;
* laisser du code mort ;
* maintenir deux comportements concurrents ;
* garder des formulaires contradictoires ;
* conserver plusieurs définitions d'un même type de bien.

Une seule règle métier est autorisée.

---

# ARTICLE 7 — HIÉRARCHIE DES RÈGLES

En cas de conflit, l'ordre de priorité est le suivant :

1. Constitution LAWIM
2. Référentiel des biens
3. Référentiel conversationnel
4. Référentiel matching
5. Référentiel workflow
6. Référentiel base de données
7. Code source

Le code est toujours le dernier niveau.

---

# ARTICLE 8 — RÈGLE DE DÉVELOPPEMENT

Aucun développeur, aucune IA, aucun outil ne peut inventer une règle métier.

Toute nouvelle règle doit :

1. être ajoutée à la Constitution ;
2. être validée ;
3. être implémentée dans le code ;
4. être couverte par des tests.

L'ordre inverse est interdit.

---

# ARTICLE 9 — RÈGLE DE QUALITÉ

Une fonctionnalité est considérée terminée uniquement si :

* elle respecte la Constitution ;
* elle ne contient aucune logique contradictoire ;
* tous les tests passent ;
* les données sont conformes ;
* les workflows sont conformes ;
* le moteur conversationnel respecte le référentiel ;
* le matching respecte le référentiel ;
* le rematching respecte le référentiel.

---

# ARTICLE 10 — OBJECTIF FINAL

L'objectif de LAWIM n'est pas de publier des annonces.

L'objectif est de résoudre complètement un besoin immobilier.

Un dossier n'est terminé que lorsque :

* le besoin est satisfait ;
* ou que toutes les possibilités conformes au référentiel ont été épuisées.

Jusqu'à cette étape, LAWIM poursuit automatiquement le suivi, la relance et, si nécessaire, le rematching.

---

# ARTICLE 11 — PRINCIPES DE CONCEPTION DU SYSTÈME

LAWIM est un système piloté par les données métier.

Le moteur conversationnel, le moteur de matching, les dashboards, les formulaires et les API ne doivent jamais contenir de logique métier propre.

Ils doivent uniquement appliquer les règles décrites dans les documents de la Constitution.

Aucune décision métier importante ne doit être codée directement dans un service ou un composant.

Les décisions métier doivent toujours être documentées avant d'être implémentées.

---

# ARTICLE 12 — ARCHITECTURE MÉTIER

LAWIM est composé des moteurs suivants.

- Workflow Engine ;
- Conversation Engine ;
- Qualification Engine ;
- Matching Engine ;
- Rematching Engine ;
- Dashboard Engine ;
- Notification Engine ;
- Geo Engine ;
- Role Engine ;
- Reporting Engine ;
- Storage Lifecycle Manager ;
- Security Engine ;
- API Gateway ;
- Administration Engine ;
- LAWIM AI ;
- Continuous Learning Engine ;
- Campay Payment Engine.

## 12.1 Moteur Conversationnel

Mission :

Comprendre le besoin réel de l'utilisateur.

Ne poser que les questions réellement utiles.

Collecter les informations critiques.

Compléter progressivement les informations facultatives.

Lancer automatiquement le matching dès que les informations critiques sont disponibles.

---

## 12.2 Moteur de Qualification

Mission :

Transformer une conversation libre en données immobilières structurées.

Le moteur doit être capable :

- d'identifier le type de bien ;
- l'opération ;
- la ville ;
- le quartier ;
- le budget ;
- les caractéristiques principales ;
- les contraintes particulières.

Il ne dépend jamais d'un formulaire.

---

## 12.3 Moteur de Matching

Mission :

Identifier les meilleurs biens compatibles avec un besoin.

Le matching ne repose jamais sur un seul critère.

Il utilise :

- les informations critiques ;
- les informations facultatives ;
- les préférences utilisateur ;
- les données géographiques ;
- la disponibilité ;
- le cycle de vie du bien.

---

## 12.4 Moteur de Rematching

Mission :

Relancer automatiquement la recherche lorsqu'un matching échoue.

Un rematching est déclenché notamment lorsque :

- le propriétaire refuse ;

- le demandeur refuse ;

- le bien devient indisponible ;

- le bien est vendu ;

- le bien est loué ;

- le propriétaire ne répond pas ;

- le délai maximal est dépassé.

Le système ne repart jamais de zéro.

Il réutilise les informations déjà connues.

---

## 12.5 Moteur de Suivi

Mission :

Accompagner le dossier jusqu'à sa clôture.

Le suivi continue après :

- la mise en relation ;

- la visite ;

- la négociation ;

- la transaction.

LAWIM ne considère pas un dossier terminé tant que son issue n'est pas connue.

---

## 12.6 Workflow Engine

Mission :

Orchestrer les transitions d'état de tous les objets métier.

Le Workflow Engine :

- applique les règles de cycle de vie ;
- déclenche les événements autorisés ;
- conserve l'historique des transitions ;
- empêche tout contournement des états officiels.

---

## 12.7 Dashboard Engine

Mission :

Afficher l'état opérationnel de LAWIM sans jamais créer de règle métier.

Le Dashboard Engine :

- présente les indicateurs ;
- expose les alertes ;
- adapte les vues au rôle ;
- ne modifie jamais la source de vérité.

---

## 12.8 Notification Engine

Mission :

Diffuser les notifications déclenchées par les événements officiels.

Le Notification Engine :

- relaie les alertes ;
- conserve l'origine ;
- respecte les permissions ;
- ne fabrique aucune décision métier.

---

## 12.9 Geo Engine

Mission :

Normaliser la localisation, calculer les proximités et structurer les zones LAWIM.

Le Geo Engine :

- normalise les villes, quartiers et repères ;
- calcule les distances ;
- alimente le matching et les dashboards.

---

## 12.10 Role Engine

Mission :

Gérer les identités, les rôles, les permissions et les appartenances organisationnelles.

Le Role Engine :

- contrôle les accès ;
- trace les responsabilités ;
- empêche les privilèges non autorisés.

---

## 12.11 Reporting Engine

Mission :

Calculer les indicateurs, les rapports et les analyses officielles de LAWIM.

Le Reporting Engine :

- produit les KPI ;
- consolide les données ;
- ne modifie jamais les données sources.

---

## 12.12 Storage Lifecycle Manager

Mission :

Gérer le stockage, l'archivage, la sauvegarde et la restauration.

Le Storage Lifecycle Manager :

- applique la politique de conservation ;
- organise les supports de stockage ;
- conserve la traçabilité des archives.

---

## 12.13 Security Engine

Mission :

Protéger les accès, les données, les documents sensibles et les secrets.

Le Security Engine :

- applique l'authentification ;
- contrôle les autorisations ;
- surveille les menaces ;
- protège les paiements et les sauvegardes.

---

## 12.14 API Gateway

Mission :

Centraliser l'entrée des API officielles.

L'API Gateway :

- applique la version ;
- contrôle le débit ;
- valide les contrats ;
- n'introduit aucune logique métier cachée.

---

## 12.15 Administration Engine

Mission :

Superviser la plateforme, les paramètres, les validations et les opérations internes.

L'Administration Engine :

- gère les tâches de supervision ;
- contrôle les actions sensibles ;
- prépare les arbitrages administratifs.

---

## 12.16 LAWIM AI

Mission :

Assister la compréhension, la recommandation et l'analyse sans remplacer la décision humaine.

LAWIM AI :

- propose ;
- résume ;
- explique ;
- n'altère jamais seule les règles métier.

---

## 12.17 Continuous Learning Engine

Mission :

Capitaliser les apprentissages mensuels et préparer les améliorations validées.

Le Continuous Learning Engine :

- analyse les résultats ;
- produit des propositions ;
- n'applique jamais automatiquement une règle critique.

---

## 12.18 Campay Payment Engine

Mission :

Gérer les paiements Mobile Money via Campay pour les services LAWIM.

Le Campay Payment Engine :

- initie les paiements ;
- vérifie les confirmations serveur à serveur ;
- active le service uniquement après confirmation ;
- ne prélève jamais de commission sur une transaction immobilière.

---

# ARTICLE 13 — RÈGLES GÉNÉRALES DE QUALIFICATION

Chaque échange utilisateur doit être analysé.

Le système doit rechercher automatiquement :

- les nouvelles informations ;

- les corrections ;

- les contradictions ;

- les changements de ville ;

- les changements de quartier ;

- les changements de budget ;

- les changements de type de bien ;

- les changements d'opération.

Une nouvelle information valide remplace immédiatement l'ancienne.

Le système ne demande jamais confirmation d'une information clairement exprimée.

---

# ARTICLE 14 — RÈGLES DE CONVERSATION

La conversation doit rester naturelle.

Le système ne doit jamais donner l'impression de remplir un formulaire.

Les questions doivent toujours être motivées.

Une seule question doit être posée à la fois.

Le système ne doit jamais demander :

- une information déjà connue ;

- une information déductible ;

- une information inutile pour le type de bien.

Le moteur doit privilégier :

- les questions courtes ;

- les formulations naturelles ;

- les relances pertinentes.

---

# ARTICLE 15 — RÈGLES D'ARRÊT DE LA QUALIFICATION

La qualification est considérée comme suffisante lorsque les champs critiques du type de bien sont connus.

À ce moment :

le matching est lancé immédiatement.

Le système peut ensuite continuer à enrichir le dossier avec des informations facultatives.

Le matching ne doit jamais attendre que tous les champs facultatifs soient renseignés.

---

# ARTICLE 16 — RÈGLES DE CORRECTION

L'utilisateur peut corriger :

- une ville ;

- un quartier ;

- un budget ;

- un type de bien ;

- une opération ;

- une caractéristique.

Toute correction écrase définitivement la valeur précédente.

Le système ne doit jamais conserver deux versions concurrentes.

Toute correction doit déclencher :

- une réévaluation de la qualification ;

- une réévaluation du matching ;

- une réévaluation des propositions.

---

# ARTICLE 17 — GESTION DES CHANGEMENTS DE BESOIN

Un utilisateur peut changer complètement de projet.

Exemple :

"Je voulais louer un studio.

Finalement je cherche une villa à acheter."

Le système doit :

- archiver l'ancien besoin ;

- ouvrir automatiquement un nouveau besoin ;

- conserver l'historique ;

- éviter toute confusion entre les deux dossiers.

Chaque besoin possède son propre historique.

---

# ARTICLE 18 — MÉMOIRE CONVERSATIONNELLE

LAWIM possède une mémoire conversationnelle.

Cette mémoire doit conserver :

- les informations déjà données ;

- les corrections ;

- les refus ;

- les préférences ;

- les biens proposés ;

- les biens refusés ;

- les visites ;

- les mises en relation.

La mémoire ne doit jamais être perdue pendant une conversation.

Elle peut être réutilisée lors d'une nouvelle interaction avec le même utilisateur.

---

# ARTICLE 19 — RÈGLES DE COHÉRENCE

Le système doit détecter les incohérences.

Exemples interdits :

- terrain avec chambres ;

- terrain avec salon ;

- terrain avec piscine comme critère principal ;

- studio de cinq chambres ;

- chambre avec quatre salons ;

- appartement sans chambre ;

- villa d'une chambre sans justification ;

- immeuble avec zéro logement.

Lorsqu'une incohérence est détectée :

le système doit demander une clarification.

Jamais enregistrer une information manifestement incohérente.

---

# ARTICLE 20 — NORMALISATION DES DONNÉES

Toutes les données doivent être normalisées.

Exemples :

"Yaounde"

"yaoundé"

"Ydé"

doivent devenir

"Yaoundé"

Les synonymes doivent être regroupés.

Les fautes courantes doivent être corrigées.

Les doublons doivent être éliminés.

Les valeurs libres doivent être transformées autant que possible en valeurs normalisées.

La normalisation constitue une étape obligatoire avant toute recherche de matching.

---

# ARTICLE 21 — GÉOLOCALISATION

Chaque bien doit pouvoir être géolocalisé.

Les coordonnées GPS constituent un champ facultatif fortement recommandé.

OpenStreetMap devient le référentiel cartographique officiel de LAWIM.

Les coordonnées GPS serviront notamment à :

- calculer les distances ;

- classer les résultats ;

- rechercher les biens proches ;

- afficher les cartes ;

- optimiser le matching géographique.

---

# ARTICLE 22 — PRINCIPES FINAUX

Ce document définit les principes fondamentaux de LAWIM.

Tous les documents suivants de la Constitution devront respecter intégralement ces principes.

Aucune règle ultérieure ne pourra contredire le présent document.

---

# ARTICLE 23 — SUPPORT MULTILINGUE

LAWIM fonctionne nativement en Français, English et Pidgin English.

La langue ne doit jamais être codée en dur dans les composants métier.

Le support multilingue s'appuie sur 30-I18N-L10N-REFERENCE.md, 30A-BUSINESS-DICTIONARY-REFERENCE.md, 30B-TRANSLATION-REFERENCE.md, 30C-LANGUAGE-DETECTION-REFERENCE.md et 30D-MULTILINGUAL-SEARCH-REFERENCE.md.

Les autres référentiels doivent utiliser les clés, préférences et traductions officielles.
